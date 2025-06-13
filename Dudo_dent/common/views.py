from django.shortcuts import render
from django.views.generic import TemplateView

from Dudo_dent.patients.forms import SearchPatientForm
from Dudo_dent.patients.models import Patient


# Create your views here.


class HomeView(TemplateView):
    template_name = 'common/home-page.html'
    form_class = SearchPatientForm

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form': self.form_class()
        })
        return kwargs


# def home_page(request):
#     form = SearchPatientForm()
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'common/home-page.html', context)
