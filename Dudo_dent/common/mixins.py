class ReturnToRedirectMixin:
    return_to_param = 'return_to'
    redirect_targets = {}

    def get_return_to_value(self):
        """Gets the return to value from the template"""
        return self.request.GET.get(self.return_to_param) or self.request.POST.get(self.return_to_param)

    def get_success_url(self):
        """Rewrites the get_success_url method"""
        return_to = self.get_return_to_value()
        return self.redirect_targets.get(return_to, self.get_default_success_url())

    def get_context_data(self, **kwargs):
        """Rewrites the get_context_data method"""
        context = super().get_context_data(**kwargs)
        context[self.return_to_param] = self.get_return_to_value()
        return context

    def get_default_success_url(self):
        """This method has to be overridden, so that the view gets a default success url"""
        raise NotImplementedError("You need to define a default_success_url")


class MainViewsMixin:
    form_class = None
    query_param = 'query'
    search_param = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form_class(),
            'query': self.request.GET.get(self.query_param,''),
        })
        return context

    def get_queryset(self):
        queryset = self.model.objects.all()
        search_value = self.request.GET.get(self.query_param)

        if search_value:
            queryset = queryset.filter(
                **{self.search_param: search_value},
            )
        return queryset