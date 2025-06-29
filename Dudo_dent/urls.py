from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Dudo_dent.common.urls')),
    path('patients/',include('Dudo_dent.patients.urls')),
    path('procedures/',include('Dudo_dent.procedures.urls')),
    path('visits/',include('Dudo_dent.visits.urls')),
    path('accounts/',include('Dudo_dent.accounts.urls')),
]
