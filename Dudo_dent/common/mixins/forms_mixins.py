class SearchMixin:
    """
    Mixin for adding basic search functionality to a Django CBV.
    - Uses 'query_param' as the GET parameter to search for.
    - Uses 'search_param' as the model field to filter against.
    - Uses '_cached_queryset' to avoid multiple database hits.
    """
    form_class = None
    query_param = 'query' #URL parameter name (....?query=Ivan)
    search_param = None
    _cached_queryset = None

    def get_search_value(self):
        return self.request.GET.get(self.query_param)

    def get_queryset(self):
        if self._cached_queryset is not None:
            return self._cached_queryset

        queryset = self.model.objects.all()
        search_value = self.get_search_value()

        if search_value:
            queryset = queryset.filter(
                **{self.search_param: search_value},
            )

        self._cached_queryset = queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': self.form_class(),
            'query': self.get_search_value() or '',
        })
        return context