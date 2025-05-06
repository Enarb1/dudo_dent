from django.urls import path
from Dudo_dent.patients import views

urlpatterns = [
    path('', views.all_patients, name='all-patients'),
    path('<slug:patient_slug>/', views.patient_details, name='patient-details'),
]