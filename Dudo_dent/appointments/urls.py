from django.urls import path, include

from Dudo_dent.appointments import views

urlpatterns = [
    path('google/test/', views.test_google_calender, name='google-test'),
    path('', views.AppointmentsMainView.as_view(), name='appointments-main'),
    path('json/', views.appointment_event_json, name='appointments-json'),
    path('add/',views.AddAppointmentView.as_view(), name='add-appointment'),
    path('<int:pk>/', include([
        path('', views.AppointmentDetailView.as_view(), name='appointment-details'),
        path('edit/', views.EditAppointmentView.as_view(), name='appointment-edit'),
        path('delete/', views.DeleteAppointmentView.as_view(), name='appointment-delete'),
    ]))
]