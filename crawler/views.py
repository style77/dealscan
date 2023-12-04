import random
from typing import Any, Dict, Optional

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from djstripe.models import Customer

from django.contrib.auth import get_user_model
from django.db.models import Subquery

from polls.models import Poll, PollAnswer

LOGIN_URL = reverse_lazy("account_login")
User = get_user_model()


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def _find_poll(self, user: User) -> Optional[Poll]:
        answered_polls = PollAnswer.objects.filter(user=user).values("poll_id")
        unanswered_polls = Poll.objects.exclude(id__in=Subquery(answered_polls))
        if not unanswered_polls:
            return None

        return random.choice(unanswered_polls)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        poll = self._find_poll(self.request.user)

        if poll:
            context.update({
                "poll_id": poll.id
            })

        return context


class BillingView(TemplateView):
    template_name = "billing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_plan_id"] = self.request.GET.get("plan_id")
        z = Customer.objects.filter(subscriber=self.request.user).first()
        subscriptions = z.subscriptions if z else None
        context["subscriptions"] = subscriptions

        return context


dashboard_view = login_required(DashboardView.as_view(), login_url=LOGIN_URL)
billing_view = login_required(BillingView.as_view(), login_url=LOGIN_URL)
