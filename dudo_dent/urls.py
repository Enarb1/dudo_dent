from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dudo_dent.common.urls')),
    path('patients/',include('dudo_dent.patients.urls')),
    path('procedures/',include('dudo_dent.procedures.urls')),
    path('visits/',include('dudo_dent.visits.urls')),
    path('accounts/',include('dudo_dent.accounts.urls')),
    path('appointments/',include('dudo_dent.appointments.urls')),
    path('api/',include('dudo_dent.appointments.api_urls')),
]
