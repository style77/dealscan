import random
from typing import Any, Dict, Optional

from django import http
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Subquery
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from djstripe.models import Customer, Product

from crawler.models import Offer
from polls.models import Poll, PollAnswer

LOGIN_URL = reverse_lazy("account_login")
User = get_user_model()


class BaseTemplateView(TemplateView):
    def _find_poll(self, user) -> Optional[Poll]:
        answered_polls = PollAnswer.objects.filter(user=user).values("poll_id")
        unanswered_polls = Poll.objects.exclude(id__in=Subquery(answered_polls))
        if not unanswered_polls:
            return None

        return random.choice(unanswered_polls)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        poll = self._find_poll(self.request.user)

        if poll:
            context.update({"poll_id": poll.id})

        return context


class DashboardView(BaseTemplateView):
    template_name = "dashboard.html"

    def _find_poll(self, user) -> Optional[Poll]:
        answered_polls = PollAnswer.objects.filter(user=user).values("poll_id")
        unanswered_polls = Poll.objects.exclude(id__in=Subquery(answered_polls))
        if not unanswered_polls:
            return None

        return random.choice(unanswered_polls)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        poll = self._find_poll(self.request.user)

        if poll:
            context.update({"poll_id": poll.id})

        return context


class OffersView(BaseTemplateView):
    template_name = "offers.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class OfferComponentView(TemplateView):
    template_name = "all_offers.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_queryset = Offer.objects.all()

        filter_params = self.request.GET
        filtered_offers = base_queryset

        all_filter_params = ["model__make", "model"]
        for param in all_filter_params:
            if param in filter_params:
                filtered_offers = filtered_offers.filter(
                    **{param: filter_params[param]}
                )

        limit = filter_params.get("limit", 40)
        if limit < 10:
            limit = 10
        elif limit > 150:
            limit = 150

        paginator = Paginator(filtered_offers.order_by("-publication_date"), limit)

        page = self.request.GET.get("page")
        try:
            offers = paginator.page(page)
        except PageNotAnInteger:
            offers = paginator.page(1)
        except EmptyPage:
            offers = paginator.page(paginator.num_pages)

        context["offers"] = offers

        return context


class BillingView(TemplateView):
    template_name = "billing.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["current_plan_id"] = self.request.GET.get("plan_id")
        z = Customer.objects.filter(subscriber=self.request.user).first()
        subscriptions = z.subscriptions if z else None
        context["subscriptions"] = subscriptions
        context["publishable_key"] = settings.STRIPE_PUBLISHABLE_KEY
        context["products"] = Product.objects.filter(active=True)

        return context

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        return super().get(request, *args, **kwargs)


dashboard_view = login_required(DashboardView.as_view(), login_url=LOGIN_URL)
billing_view = login_required(BillingView.as_view(), login_url=LOGIN_URL)
offers_view = login_required(OffersView.as_view(), login_url=LOGIN_URL)
all_offers_view = login_required(OfferComponentView.as_view(), login_url=LOGIN_URL)
