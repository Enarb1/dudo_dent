from django.urls import path
from Dudo_dent.common import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

]
