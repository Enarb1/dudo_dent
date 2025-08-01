from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include

from Dudo_dent.accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('all-accounts/', views.AccountsListView.as_view(), name='all-accounts'),
    path('<int:pk>/', include([
        path('', views.UserProfileView.as_view(), name='profile'),
        path('edit/', views.EditProfileView.as_view(), name='edit-profile'),
        path('delete/', views.DeleteProfileView.as_view(), name='delete-profile'),
        path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    ]) ),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done')

]



