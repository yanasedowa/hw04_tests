from django.conf import settings
from django.core.paginator import Paginator


def posts_paginator(request, posts):

    paginator = Paginator(posts, settings.LAST_TEN)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj
