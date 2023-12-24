from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _


class DemoModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return HttpResponseForbidden(_("This action is not allowed in demo mode."))
        return self.get_response(request)
