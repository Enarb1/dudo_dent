from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate_queryset(request, queryset, per_page=10, context_key='page_obj'):
    """
    A custom pagination function which is used in View, which don't have
    the integrated pagination. We pass {'page_obj': page_obj} and {context_key: page_obj}.
    {'page_obj': page_obj} is used for Django's pagination tools.
    {context_key: page_obj} so that our own template can loop at the custom set object list.
    Returns a dictionary
    """

    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return {
        'paginator': paginator,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        context_key: page_obj,
    }
