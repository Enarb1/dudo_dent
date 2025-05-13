from django.urls import path, include
from Dudo_dent.patients import views

urlpatterns = [
    path('', views.all_patients, name='all-patients'),
    path('add-patient/', views.add_patient, name='add-patient'),
    path('<slug:patient_slug>/', include([
        path('',views.patient_details, name='patient-details'),
        path('edit-patient/', views.edit_patient, name='edit-patient'),
        path('delete-patient/', views.delete_patient, name='delete-patient'),
    ]))
]