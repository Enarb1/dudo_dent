from django.shortcuts import render

from Dudo_dent.patients.forms import SearchPatientForm
from Dudo_dent.patients.models import Patient


# Create your views here.

def home_page(request):
    form = SearchPatientForm()

    context = {
        'form': form,
    }

    return render(request, 'common/home-page.html', context)
