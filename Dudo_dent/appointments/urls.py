from django.urls import path, include

from Dudo_dent.appointments import views

urlpatterns = [
    path('google/test/', views.test_google_calender, name='google-test'),
    path('', views.AppointmentsMainView.as_view(), name='appointments-main'),
    path('add/',views.AddAppointmentView.as_view(), name='add-appointment'),
]