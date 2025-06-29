from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from Dudo_dent.common.mixins import ReturnToRedirectMixin, MainViewsMixin, EditDataMixin
from Dudo_dent.patients.forms import PatientCreateForm, PatientEditForm, SearchPatientForm
from Dudo_dent.patients.models import Patient


# Create your views here.

class AllPatientsView(MainViewsMixin, ListView):
    model = Patient
    template_name = 'patients/patients-main.html'
    form_class = SearchPatientForm
    search_param = 'full_name__icontains'

    def get_queryset(self):
        return super().get_queryset().order_by('full_name')


    # query_param = 'query'
    #
    # def get_context_data(self, *, object_list =None, **kwargs):
    #     kwargs.update({
    #         'form': self.form_class(),
    #         'query': self.request.GET.get(self.query_param,'')
    #     })
    #
    #     return super().get_context_data(object_list=object_list,**kwargs)
    #
    # def get_queryset(self):
    #     queryset = self.model.objects.all()
    #     search_value = self.request.GET.get(self.query_param)
    #
    #     if search_value:
    #         queryset = queryset.filter(
    #             full_name__icontains=search_value,
    #         )
    #
    #     return queryset.order_by('full_name')

class PatientDetailsView(DetailView):
    model = Patient
    template_name = 'patients/patient-details.html'
    slug_field = 'slug'
    slug_url_kwarg = 'patient_slug'

    def get_context_data(self,**kwargs):
        visits = self.object.visits.all().order_by('-date')
        kwargs.update({
            'visits':visits
        })

        return super().get_context_data(**kwargs)


class PatientCreateView(ReturnToRedirectMixin, CreateView):
    model = Patient
    form_class = PatientCreateForm
    template_name = 'patients/add-patient.html'
    return_to_param = 'return_to'
    redirect_targets = {
        'add-visit': reverse_lazy('add-visit'),
    }

    def get_default_success_url(self):
        return reverse_lazy('all-patients')

    def form_valid(self, form):
        super().form_valid(form)
        #TODO get the dentist id from the request data

class EditPatientView(EditDataMixin, UpdateView):
    model = Patient
    form_class = PatientEditForm
    template_name = 'patients/edit-patient.html'
    redirect_url = 'patient-details'
    context_param = 'patient'
    get_object_by = 'slug'
    slug_param = 'patient_slug'


    def get_object(self, queryset=None):
        return self.model.objects.filter(
            slug=self.kwargs[self.slug_param]
            ).first()

class DeletePatientView(DeleteView):
    # with conformation form
    model = Patient
    template_name = 'patients/delete-conformation.html'
    slug_field = 'slug'
    slug_url_kwarg = 'patient_slug'
    success_url = reverse_lazy('all-patients')










