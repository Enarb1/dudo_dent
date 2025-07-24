from django.urls import path, include

from Dudo_dent import appointments
from Dudo_dent.appointments import views

urlpatterns = [
    #path('google/test/', views.test_google_calender, name='google-test'),
    path('', views.AppointmentsMainView.as_view(), name='appointments-main'),
    path('availability/', views.SetAvailabilityView.as_view(), name='availability'),
    path('json/', views.appointment_event_json, name='appointments-json'),
    path('add/',include([
        path('step1/', views.ChooseDentistView.as_view(), name='appointment-step1'),
        path('step2/', views.ChooseDateView.as_view(), name='appointment-step2'),
        path('step3/', views.ChooseTimeView.as_view(), name='appointment-step3'),
    ])),
    path('<int:pk>/', include([
        path('', views.AppointmentDetailView.as_view(), name='appointment-details'),
        path('edit/', views.EditAppointmentView.as_view(), name='appointment-edit'),
        path('delete/', views.DeleteAppointmentView.as_view(), name='appointment-delete'),
    ]))
]