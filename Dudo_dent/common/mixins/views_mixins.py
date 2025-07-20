from django.urls import reverse_lazy


class EditDataMixin:
    """Edit Mixin , which can be used together with the UpdateView.
    We define the value and the look-up field for the object.
    We can redefine the pk_url_kwarg from the UpdateView class.
    We define the redirect_url and the context data.
    """
    redirect_url = None
    get_object_by = 'pk'
    pk_url_kwarg = 'pk'
    context_param = None

    def get_success_url(self):
        return reverse_lazy(self.redirect_url, kwargs={
           self.pk_url_kwarg: getattr(self.object, self.get_object_by),
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_param] = self.object

        return context

    def get_object(self):
        lookup_by_field = self.get_object_by
        lookup_value = self.kwargs.get(self.pk_url_kwarg)
        return self.model.objects.filter(**{lookup_by_field: lookup_value}).first()


class DeleteCancelMixIn:
        cancel_url = None
        cancel_url_kwarg_field = 'pk'

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            if not self.cancel_url:
                raise ValueError("You need to define a 'cancel url' in your DeleteCancelMixin!")

            obj = self.get_object()
            cancel_kwargs = {self.cancel_url_kwarg_field: getattr(obj, self.cancel_url_kwarg_field)}
            context['cancel_url'] = reverse_lazy(self.cancel_url, kwargs=cancel_kwargs)

            return context




















