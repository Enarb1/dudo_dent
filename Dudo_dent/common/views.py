from django.views.generic import TemplateView

from Dudo_dent.appointments.utils import get_appointments_for_today
from Dudo_dent.patients.forms import SearchPatientForm

# Create your views here.


class HomeView(TemplateView):
    template_name = 'common/home.html'
    form_class = SearchPatientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        context['appointments'] = get_appointments_for_today(self.request.user)
        return context

