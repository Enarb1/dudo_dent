
from django.urls import path

from Dudo_dent.appointments.views import AppointmentListAPIView

urlpatterns = [
    path('calendar/', AppointmentListAPIView.as_view(), name='calendar'),
]