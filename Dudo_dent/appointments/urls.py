from django.urls import path, include

from Dudo_dent.appointments import views

urlpatterns = [
    path('', views.AppointmentsMainView.as_view(), name='appointments-main'),
    path('availability/', views.SetAvailabilityView.as_view(), name='availability'),
    path('unavailability/', views.SetUnavailabilityView.as_view(), name='unavailability'),
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