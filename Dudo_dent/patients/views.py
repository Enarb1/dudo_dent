from django.shortcuts import render, redirect, get_object_or_404

from Dudo_dent.patients.forms import PatientCreateForm, PatientEditForm, SearchPatientForm
from Dudo_dent.patients.models import Patient


# Create your views here.

def all_patients(request):

    patients = Patient.objects.all().order_by('full_name')
    form = SearchPatientForm(request.GET)

    if request.method == 'GET':
        if form.is_valid():
            query = form.cleaned_data['query']
            patients = patients.filter(full_name__icontains=query).order_by('full_name')


    context = {
        'patients': patients,
        'form': form
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


def add_patient(request):
    form = PatientCreateForm(request.POST or None)
    return_to = request.GET.get('return_to') or request.POST.get('return_to')

    if request.method == 'POST' and form.is_valid():
        form.save()

        if return_to == 'add-visit':
            return redirect('add-visit')
        return redirect('all-patients')

    context = {
        'form': form,
        'return_to': return_to
    }

    return render(request, 'patients/add-patient.html', context)

def edit_patient(request, patient_slug: str):
    patient = Patient.objects.filter(slug=patient_slug).first()

    if request.method == 'POST':
        form = PatientEditForm(request.POST,instance=patient)

        if form.is_valid():
            form.save()

            return redirect('patient-details', patient_slug=patient.slug)
    else:
        form = PatientEditForm(instance=patient)

    context = {
        'form': form,
        'patient': patient
    }

    return render(request,'patients/edit-patient.html', context)



def delete_patient(request, patient_slug: str):
    patient = get_object_or_404(Patient, slug=patient_slug)
    if request.method == 'POST':
        patient.delete()
        return redirect('all-patients')

    return redirect('patient-details', patient_slug=patient.slug)









