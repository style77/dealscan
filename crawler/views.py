from typing import Any
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy("account_login")


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context


dashboard_view = login_required(DashboardView.as_view(), login_url=LOGIN_URL)
billing_view = login_required(DashboardView.as_view(), login_url=LOGIN_URL)
