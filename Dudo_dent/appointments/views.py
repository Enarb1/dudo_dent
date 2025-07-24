from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.constants import APPOINTMENT_FIELDS
from Dudo_dent.accounts.services.profile_display import get_profile_fields
from Dudo_dent.appointments.forms import EditAppointmentForm,SetAvailabilityForm, \
    AddAppointmentChooseDentistForm, AddAppointmentChooseDateForm, AddAppointmentChooseTimeForm
from Dudo_dent.appointments.google_calendar import add_appointment_to_google_calendar
from Dudo_dent.appointments.models import Appointment, AvailabilityRule
from Dudo_dent.appointments.permissions import has_calender_access
from Dudo_dent.appointments.utils import clear_booking_session, get_dentist_available_dates, get_available_time_slots
from Dudo_dent.common.mixins.permissions_mixins import RoleRequiredMixin, \
    AppointmentAccessMixin
from Dudo_dent.common.mixins.views_mixins import EditDataMixin, DeleteCancelMixIn



UserModel = get_user_model()
# Create your views here.

class AppointmentsMainView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointments-main.html'
    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.NURSE]


class ChooseDentistView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'appointments/book-appointment/appointment-step1.html'
    form_class = AddAppointmentChooseDentistForm

    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.PATIENT, UserTypeChoices.NURSE]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user

        return kwargs

    def form_valid(self, form):
        self.request.session['patient_id'] = form.cleaned_data['patient'].id
        self.request.session['dentist_id'] = form.cleaned_data['dentist'].id
        return redirect('appointment-step2')


class ChooseDateView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'appointments/book-appointment/appointment-step2.html'
    form_class = AddAppointmentChooseDateForm

    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.PATIENT, UserTypeChoices.NURSE]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        dentist_id = self.request.session.get('dentist_id')
        available_dates = get_dentist_available_dates(dentist_id) if dentist_id else []

        kwargs['available_dates'] = available_dates
        return kwargs

    def form_valid(self, form):
        self.request.session['date'] =  form.cleaned_data['date'].isoformat()
        return redirect('appointment-step3')


class ChooseTimeView(LoginRequiredMixin, RoleRequiredMixin, FormView):
    template_name = 'appointments/book-appointment/appointment-step3.html'
    form_class = AddAppointmentChooseTimeForm
    success_url = reverse_lazy('home')

    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.PATIENT, UserTypeChoices.NURSE]

    def _get_booking_context(self):
        patient_id = self.request.session.get('patient_id')
        dentist_id = self.request.session.get('dentist_id')
        date_str = self.request.session.get('date')
        date_object = date.fromisoformat(date_str) if date_str else None

        return patient_id, dentist_id, date_object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        _, dentist_id, date_object = self._get_booking_context()
        if dentist_id and date_object:
            kwargs['available_times'] = get_available_time_slots(dentist_id, date_object)

        return kwargs

    def form_valid(self, form):
        patient_id, dentist_id, appointment_date = self._get_booking_context()
        start_time = form.cleaned_data['start_time']

        if not (patient_id and dentist_id and date):
            return redirect('appointment-step1')

        patient = UserModel.objects.filter(pk=patient_id).first()
        dentist = UserModel.objects.filter(pk=dentist_id).first()

        appointment = Appointment.objects.create(
            date=appointment_date,
            start_time=start_time,
            patient=patient,
            dentist=dentist,
        )

        add_appointment_to_google_calendar(appointment, dentist, patient)

        clear_booking_session(self.request.session)
        return super().form_valid(form)


class AppointmentDetailView(LoginRequiredMixin, AppointmentAccessMixin, DetailView):
    model = Appointment
    template_name = 'appointments/appointment-details.html'

    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.NURSE]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()
        field_map = APPOINTMENT_FIELDS

        """We are using the appointment as profile, 
        so that we can user get_profile_fields to get the fields dynamically"""
        context['profile_fields'] = get_profile_fields(field_map, appointment, None)

        return context

#TODO edit appointment in Google Calendar
class EditAppointmentView(LoginRequiredMixin, RoleRequiredMixin,  EditDataMixin, UpdateView):
    model = Appointment
    form_class = EditAppointmentForm
    template_name = 'appointments/edit-appointment.html'

    get_object_by = 'pk'
    redirect_url = 'appointment-details'
    context_param = 'appointment'

    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.NURSE]

#TODO delete appointment in Google Calendar
class DeleteAppointmentView(LoginRequiredMixin, RoleRequiredMixin,DeleteCancelMixIn, DeleteView):
    model = Appointment
    template_name = 'delete-conformation.html'
    cancel_url = 'appointment-details'

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def get_success_url(self):
        return reverse_lazy('home')


class SetAvailabilityView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    """
    Setting the availability time for a period.
    If there are overlapping days in an overlapping period,
    those days are updated or moved.
    If the entire set matches, the old rule is deleted.
    """
    model = AvailabilityRule
    form_class = SetAvailabilityForm
    template_name = 'appointments/set-availability.html'

    allowed_roles = [UserTypeChoices.DENTIST]

    @staticmethod
    def _remove_overlapping_days(overlapping_rules, new_weekdays):
        for rule in overlapping_rules:
            existing_weekdays = set(rule.weekdays)
            overlapping_weekdays = existing_weekdays.intersection(new_weekdays)

            if overlapping_weekdays:
                remaining_days = existing_weekdays - overlapping_weekdays

                if remaining_days:
                    rule.weekdays = list(remaining_days)
                    rule.save()
                else:
                    rule.delete()

    def form_valid(self, form):
        user = self.request.user
        form.instance.dentist = user

        new_weekdays = form.cleaned_data['weekdays']
        new_from = form.cleaned_data['valid_from']
        new_to = form.cleaned_data['valid_to']

        overlapping_rules = AvailabilityRule.objects.filter(
            dentist_id=user.id,
            valid_from__lte=new_to,
            valid_to__gte=new_from,
        )

        self._remove_overlapping_days(overlapping_rules, new_weekdays)

        form.instance.weekdays = new_weekdays

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})


@user_passes_test(has_calender_access)
@login_required
def appointment_event_json(request):
    """
    Full Calendar settings
    """

    appointments = Appointment.objects.all()

    events = [{
            'title': f'{a.patient}',
            'start': f'{a.date.isoformat()}T{a.start_time.strftime("%H:%M:%S")}',
            'end': f'{a.date.isoformat()}T{a.end_time.strftime("%H:%M:%S")}' if a.end_time else None,
            'url': a.get_absolute_url(),
    } for a in appointments]

    return JsonResponse(events, safe=False)


#
# def test_google_calender(request):
#     service = get_calendar_service()
#     calender = service.calendars().get(calendarId=settings.GOOGLE_CALENDAR_ID).execute()
#     return JsonResponse({'summary': calender.get('summary')})
