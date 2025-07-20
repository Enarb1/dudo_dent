from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from Dudo_dent.accounts.choices import UserTypeChoices
from Dudo_dent.accounts.constants import APPOINTMENT_FIELDS
from Dudo_dent.accounts.services.profile_display import get_profile_fields
from Dudo_dent.appointments.forms import AddAppointmentForm, EditAppointmentForm, DeleteAppointmentForm
from Dudo_dent.appointments.google_calender import get_calender_service
from Dudo_dent.appointments.models import Appointment
from Dudo_dent.appointments.permissions import has_calender_access
from Dudo_dent.common.mixins.permissions_mixins import RoleRequiredMixin, \
    AppointmentAccessMixin
from Dudo_dent.common.mixins.views_mixins import EditDataMixin, DeleteCancelMixIn


# Create your views here.

class AppointmentsMainView(LoginRequiredMixin, RoleRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointments-main.html'
    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.NURSE]


class AddAppointmentView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Appointment
    form_class = AddAppointmentForm
    template_name = 'appointments/add-appointment.html'
    success_url = reverse_lazy('home')

    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.PATIENT, UserTypeChoices.NURSE]

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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


class EditAppointmentView(LoginRequiredMixin, RoleRequiredMixin,  EditDataMixin, UpdateView):
    model = Appointment
    form_class = EditAppointmentForm
    template_name = 'appointments/edit-appointment.html'

    get_object_by = 'pk'
    redirect_url = 'appointment-details'
    context_param = 'appointment'

    allowed_roles = [UserTypeChoices.DENTIST, UserTypeChoices.NURSE]


class DeleteAppointmentView(LoginRequiredMixin, RoleRequiredMixin,DeleteCancelMixIn, DeleteView):
    model = Appointment
    template_name = 'delete-conformation.html'
    cancel_url = 'appointment-details'

    allowed_roles = [UserTypeChoices.NURSE, UserTypeChoices.DENTIST]

    def get_success_url(self):
        return reverse_lazy('home')


@user_passes_test(has_calender_access)
@login_required
def appointment_event_json(request):
    appointments = Appointment.objects.all()

    events = [{
            'title': f'{a.patient}',
            'start': f'{a.date.isoformat()}T{a.start_time.strftime("%H:%M:%S")}',
            'end': f'{a.date.isoformat()}T{a.end_time.strftime("%H:%M:%S")}' if a.end_time else None,
            'url': a.get_absolute_url(),
    } for a in appointments]

    return JsonResponse(events, safe=False)



def test_google_calender(request):
    service = get_calender_service()
    calender = service.calendars().get(calendarId=settings.GOOGLE_CALENDAR_ID).execute()
    return JsonResponse({'summary': calender.get('summary')})
