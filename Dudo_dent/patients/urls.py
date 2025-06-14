from django.urls import path, include
from Dudo_dent.patients import views
urlpatterns = [
    path('', views.AllPatientsView.as_view(), name='all-patients'),
    path('add-patient/', views.PatientCreateView.as_view(), name='add-patient'),
    path('<slug:patient_slug>/', include([
        path('',views.PatientDetailsView.as_view(), name='patient-details'),
        path('edit-patient/', views.EditPatientView.as_view(), name='edit-patient'),
        path('delete-patient/', views.DeletePatientView.as_view(), name='delete-patient'),
    ]))
]