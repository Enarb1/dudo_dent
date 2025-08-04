from django.views.generic import TemplateView

from dudo_dent.appointments.utils import get_appointments_for_today
from dudo_dent.common.utils import paginate_queryset
from dudo_dent.patients.forms import SearchPatientForm

import logging
logger = logging.getLogger(__name__)

# Create your views here.

class HomeView(TemplateView):
    template_name = 'common/home.html'
    form_class = SearchPatientForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()

        appointments = get_appointments_for_today(self.request.user)

        pagination_context = paginate_queryset(
            self.request,
            appointments,
            per_page=10,
            context_key='appointments',
        )

        context.update(pagination_context)

        return context

