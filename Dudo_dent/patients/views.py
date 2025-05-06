from django.shortcuts import render

from Dudo_dent.patients.models import Patient


# Create your views here.

def all_patients(request):

    patients = Patient.objects.all().order_by('full_name')

    context = {
        'patients': patients
    }

    return render(request, 'patients/patients-main.html', context)


def patient_details(request, patient_slug: str):
    patient = Patient.objects.filter(slug=patient_slug).first()
    patient_visits = patient.visits.all().order_by('-date')

    context = {
        'patient': patient,
        'patient_visits': patient_visits
    }

    return render(request, 'patients/patient-details.html', context)