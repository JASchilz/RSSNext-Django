"""
Django decorators for the RSSNext project.
"""
from django.shortcuts import redirect
from django.conf import settings


def anonymous_required(func):
    """
    A decorator which only allows visitors who are not logged in.
    """

    def as_view(request, *args, **kwargs):
        """
        Redirects those visitors who are logged in to the home page.
        """

        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response
    return as_view
