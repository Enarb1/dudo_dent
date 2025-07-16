from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView

from Dudo_dent.appointments.forms import AddAppointmentForm
from Dudo_dent.appointments.google_calender import get_calender_service
from Dudo_dent.appointments.models import Appointment


# Create your views here.

class AppointmentsMainView(ListView):
    model = Appointment
    template_name = 'appointments/appointments-main.html'


class AddAppointmentView(CreateView):
    model = Appointment
    form_class = AddAppointmentForm
    template_name = 'appointments/add-appointment.html'


def test_google_calender(request):
    service = get_calender_service()
    calender = service.calendars().get(calendarId=settings.GOOGLE_CALENDAR_ID).execute()
    return JsonResponse({'summary': calender.get('summary')})
