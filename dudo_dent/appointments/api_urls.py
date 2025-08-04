
from django.urls import path

from dudo_dent.appointments.views import AppointmentListAPIView

urlpatterns = [
    path('calendar/', AppointmentListAPIView.as_view(), name='calendar'),
]