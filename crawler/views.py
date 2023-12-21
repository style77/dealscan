import random
from typing import Any, Dict, Optional

import stripe
from django import http
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Subquery
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from djstripe import models
from djstripe import settings as djstripe_settings
from djstripe.models import Product

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

        # get next billing date
        customer, _ = models.Customer.get_or_create(self.request.user)
        subscription = models.Subscription.objects.filter(customer=customer).first()
        context["next_billing_date"] = subscription.current_period_end if subscription else "Never"

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

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        key = models.APIKey.objects.filter(livemode=settings.STRIPE_LIVE_MODE).first()
        if not key:
            raise ValueError("No API key found")
        stripe.api_key = key.secret

    def initialize_checkout(
        self, request: http.HttpRequest, price_id: str, customer: models.Customer
    ) -> str:
        return_url = (
            request.build_absolute_uri(reverse("dashboard_billing"))
            + "?session_id={CHECKOUT_SESSION_ID}"
        )
        metadata = {
            f"{djstripe_settings.djstripe_settings.SUBSCRIBER_CUSTOMER_KEY}": customer.subscriber.id
        }

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer=customer.id,
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    },
                ],
                ui_mode="embedded",
                mode="subscription",
                return_url=return_url,
                metadata=metadata,
            )

        except models.Customer.DoesNotExist:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    },
                ],
                ui_mode="embedded",
                mode="subscription",
                return_url=return_url,
                metadata=metadata,
            )

        return session.client_secret

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        price_id = self.request.GET.get("plan_id")
        session_id = self.request.GET.get("session_id")

        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLISHABLE_KEY
        context["products"] = Product.objects.filter(active=True)

        customer, _ = models.Customer.get_or_create(self.request.user)

        if price_id:
            context["client_secret"] = self.initialize_checkout(
                self.request, price_id, customer
            )

        context["subscriptions"] = models.Subscription.objects.filter(customer=customer)

        if session_id:
            session = stripe.checkout.Session.retrieve(session_id)
            context["payment_status"] = session.status

        return context

    def get(
        self, request: http.HttpRequest, *args: Any, **kwargs: Any
    ) -> http.HttpResponse:
        return super().get(request, *args, **kwargs)


dashboard_view = login_required(DashboardView.as_view(), login_url=LOGIN_URL)
billing_view = login_required(BillingView.as_view(), login_url=LOGIN_URL)
offers_view = login_required(OffersView.as_view(), login_url=LOGIN_URL)
all_offers_view = login_required(OfferComponentView.as_view(), login_url=LOGIN_URL)
