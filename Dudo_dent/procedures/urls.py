from django.urls import path

from Dudo_dent.procedures import views
urlpatterns = [
    path('', views.all_procedures, name='all-procedures'),
    path('<int:pk>/', views.procedure_details, name='procedure-details'),
]