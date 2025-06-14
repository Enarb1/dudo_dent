from django.shortcuts import redirect
from django.urls import reverse_lazy


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


class MultiStepRedirectMixin:
    redirect_actions = {}
    session_key = None
    return_to_value = None

    def get_form_kwargs(self):
        """We check if there is data from the form and inject it. Also we remove the data from the session"""
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET' and self.session_key in self.request.session:
            kwargs['data'] = self.request.session.pop(self.session_key)
        return kwargs

    def post(self, request, *args, **kwargs):
        for action_name, redirect_view in self.redirect_actions.items():
            if action_name in request.POST:
                request.session[self.session_key] = request.POST
                return redirect(
                    reverse_lazy(redirect_view) + f'?{self.return_to_param}={self.return_to_value}'
                )
        
        return super().post(request, *args, **kwargs)



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














