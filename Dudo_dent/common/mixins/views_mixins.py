from django.urls import reverse_lazy


class EditDataMixin:
    redirect_url = None
    get_object_by = 'pk'
    slug_param = 'pk'
    context_param = None

    def get_success_url(self):
        return reverse_lazy(self.redirect_url, kwargs={
           self.slug_param: getattr(self.object, self.get_object_by),
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_param] = self.object

        return context