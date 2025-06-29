from django.views.generic import TemplateView
from Dudo_dent.patients.forms import SearchPatientForm

# Create your views here.


class HomeView(TemplateView):
    template_name = 'common/home.html'
    form_class = SearchPatientForm

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.form_class()
        })
        return kwargs

