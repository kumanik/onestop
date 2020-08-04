from django.conf import settings
from django.shortcuts import redirect


class StaffRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated as staff to view any 
    page other than LOGIN_URL. Exemptions to this requirement can optionally be 
    specified in settings via a list of regular expressions in LOGIN_EXEMPT_URLS
    (which you can copy from your urls.py).
    Requires authentication middleware and template context processors to be
    loaded.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path_info in settings.LOGIN_EXEMPT_URLS:
            return None
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        elif (request.user.is_authenticated) and (not request.user.is_staff):
            return redirect(settings.LOGIN_REDIRECT_URL)
        return None
