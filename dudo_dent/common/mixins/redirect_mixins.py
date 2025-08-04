from django.shortcuts import redirect
from django.urls import reverse_lazy


class ReturnToRedirectMixin:
    """
    Used for custom redirection after submitting a form. Used for forms which can have multiple success urls
    """

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


class MultiStepRedirectMixin:
    """
    Multi-step redirect mixin used for storing the data between multiple step forms.
    """

    redirect_actions = {}
    return_to_param = 'return_to'
    session_key = None
    return_to_value = None

    def get_form_kwargs(self):
        """We check if there is data from the form and inject it. Also we remove the data from the session"""
        kwargs = super().get_form_kwargs()
        if self.request.method == 'GET':
            form_data = self.request.session.pop(self.session_key, None)
            if form_data:
                kwargs['data'] = form_data

        return kwargs

    def post(self, request, *args, **kwargs):
        """Here we save the current form data into the session. Then we redirect to the corresponding
        view which we have set in the view"""
        for action_name, redirect_view in self.redirect_actions.items():
            if action_name in request.POST:
                request.session[self.session_key] = request.POST.dict()
                return redirect(
                    reverse_lazy(redirect_view) + f'?{self.return_to_param}={self.return_to_value}'
                )
        return super().post(request, *args, **kwargs)