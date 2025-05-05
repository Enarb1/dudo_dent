from django.urls import path
from Dudo_dent.common import views

urlpatterns = [
    path('',views.home_page, name='home'),
]
