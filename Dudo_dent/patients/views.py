from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

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


class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = 'patients/add-patient.html'

    def get_success_url(self):
        return_to = self.request.GET.get('return_to') or self.request.POST.get('return_to')
        if return_to == 'add-visit':
            return reverse_lazy('add-visit')

        return reverse_lazy('all-patients')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['return_to'] = self.request.GET.get('return_to') or self.request.POST.get('return_to')
        return context


# def add_patient(request):
#     form = PatientCreateForm(request.POST or None)
#     return_to = request.GET.get('return_to') or request.POST.get('return_to')
#
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#
#         if return_to == 'add-visit':
#             return redirect('add-visit')
#         return redirect('all-patients')
#
#     context = {
#         'form': form,
#         'return_to': return_to
#     }
#
#     return render(request, 'patients/add-patient.html', context)

class EditPatientView(UpdateView):
    model = Patient
    form_class = PatientEditForm
    template_name = 'patients/edit-patient.html'


    def get_object(self, queryset=None):
        return Patient.objects.filter(slug=self.kwargs['patient_slug']).first()

    def get_success_url(self):
        return reverse_lazy('patient-details', kwargs={'patient_slug': self.kwargs['patient_slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object
        return context



# def edit_patient(request, patient_slug: str):
#     patient = Patient.objects.filter(slug=patient_slug).first()
#
#     if request.method == 'POST':
#         form = PatientEditForm(request.POST,instance=patient)
#
#         if form.is_valid():
#             form.save()
#
#             return redirect('patient-details', patient_slug=patient.slug)
#     else:
#         form = PatientEditForm(instance=patient)
#
#     context = {
#         'form': form,
#         'patient': patient
#     }
#
#     return render(request,'patients/edit-patient.html', context)


class DeletePatientView(DeleteView):
    # with conformation form
    model = Patient
    template_name = 'patients/delete-conformation.html'
    slug_field = 'slug'
    slug_url_kwarg = 'patient_slug'
    success_url = reverse_lazy('all-patients')


    # without conformation form
    # def post(self, request,*args, **kwargs):
    #     patient = get_object_or_404(Patient, slug=self.kwargs['patient_slug'])
    #     patient.delete()
    #     return redirect('all-patients',)
    #
    # def get(self, *args, **kwargs):
    #     return redirect('patient-details', patient_slug=self.kwargs['patient_slug'])
#
# def delete_patient(request, patient_slug: str):
#     patient = get_object_or_404(Patient, slug=patient_slug)
#     if request.method == 'POST':
#         patient.delete()
#         return redirect('all-patients')
#
#     return redirect('patient-details', patient_slug=patient.slug)









