from django.urls import path
from Dudo_dent.patients import views

urlpatterns = [
    path('', views.all_patients, name='all-patients'),
]