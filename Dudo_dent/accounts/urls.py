from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from Dudo_dent.accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>/', include([
        path('', views.UserProfileView.as_view(), name='profile'),
    ]) ),

]