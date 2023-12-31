from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

EXEMPT_PATHS = [
    "/accounts/login/",
    "/admin/login/"
]


class DemoModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if request.path not in EXEMPT_PATHS and not request.user.is_superuser:
                return HttpResponseForbidden(
                    _("This action is not allowed in demo mode.")
                )
        return self.get_response(request)
