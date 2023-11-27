from typing import Any, Dict, List, Optional

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from djstripe.models import Customer, Subscription

LOGIN_URL = reverse_lazy("account_login")


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return context


class BillingView(TemplateView):
    template_name = "billing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_plan_id"]: Optional[str] = self.request.GET.get("plan_id")
        z = Customer.objects.filter(subscriber=self.request.user).first()
        subscriptions = z.subscriptions if z else None
        context["subscriptions"]: Optional[List[Subscription]] = subscriptions

        return context


dashboard_view = login_required(DashboardView.as_view(), login_url=LOGIN_URL)
billing_view = login_required(BillingView.as_view(), login_url=LOGIN_URL)
