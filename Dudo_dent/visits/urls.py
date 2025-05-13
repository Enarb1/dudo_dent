from django.urls import path
from Dudo_dent.visits import views
urlpatterns = [
    path('', views.all_visits, name='all-visits'),
    path('<int:pk>/', views.visit_by_id, name='visit-details'),
]