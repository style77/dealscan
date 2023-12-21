import random
from collections import namedtuple
from typing import Any, Dict, List, Optional

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

from crawler.models import Offer, OfferMetadata
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
        context["next_billing_date"] = (
            subscription.current_period_end if subscription else "Never"
        )

        return context


class OffersView(BaseTemplateView):
    template_name = "offers.html"

    def clear_params(self, params: List[str]) -> List[str]:
        return [param for param in params if param != ""]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        current_selected_makes = self.clear_params(self.request.GET.getlist("makes"))
        context["current_selected_makes"] = current_selected_makes
        current_selected_models = self.clear_params(self.request.GET.getlist("models"))
        context["current_selected_models"] = current_selected_models

        current_selected_years = self.clear_params(self.request.GET.getlist("years"))
        context["current_selected_years"] = current_selected_years
        current_selected_colors = self.clear_params(self.request.GET.getlist("colors"))
        context["current_selected_colors"] = current_selected_colors

        context["makes"] = self.__get_make_data()
        context["models"] = self.__get_model_data(current_selected_makes)
        context["years"] = self.__get_production_year(
            current_selected_makes, current_selected_models
        )
        context["colors"] = self.__get_colors(
            current_selected_makes, current_selected_models
        )
        context["transmissions"] = Offer.objects.values_list("transmission")

        context["sources"] = Offer.objects.values_list("source")

        context["forward_params"] = self.request.GET.urlencode()

        return context

    def __get_make_data(self) -> List[Any]:
        Make = namedtuple("Make", ["name"])
        makes = Offer.objects.values_list("model__make__name", flat=True).distinct()
        make_objects = [Make(name=make) for make in makes]
        return sorted(make_objects, key=lambda x: x.name)

    def __get_model_data(
        self, current_selected_makes: Optional[List[str]]
    ) -> List[Any]:
        Model = namedtuple("Model", ["name"])
        models = (
            Offer.objects.filter(model__make__name__in=current_selected_makes)
            .values_list("model__name", flat=True)
            .distinct()
            if current_selected_makes
            else Offer.objects.values_list("model__name", flat=True).distinct()
        )
        model_objects = [Model(name=model) for model in models]
        return sorted(model_objects, key=lambda x: x.name)

    def __get_production_year(
        self,
        current_selected_makes: Optional[List[str]],
        current_selected_model: Optional[List[str]],
    ) -> List[Any]:
        ProductionYear = namedtuple("ProductionYear", ["year"])
        production_years = (
            Offer.objects.filter(
                model__make__name__in=current_selected_makes,
                model__name__in=current_selected_model,
            )
            .values_list("production_year", flat=True)
            .distinct()
            if current_selected_makes and current_selected_model
            else Offer.objects.filter(model__make__name__in=current_selected_makes)
            .values_list("production_year", flat=True)
            .distinct()
            if current_selected_makes
            else Offer.objects.filter(model__name__in=current_selected_model)
            .values_list("production_year", flat=True)
            .distinct()
            if current_selected_model
            else Offer.objects.values_list("production_year", flat=True).distinct()
        )
        production_year_objects = [
            ProductionYear(year=production_year) for production_year in production_years
        ]
        return sorted(production_year_objects, key=lambda x: x.year, reverse=True)

    def __get_colors(
        self,
        current_selected_makes: Optional[List[str]],
        current_selected_model: Optional[List[str]],
    ) -> List[Any]:
        Color = namedtuple("Color", ["color"])
        colors = (
            Offer.objects.filter(
                model__make__name__in=current_selected_makes,
                model__name__in=current_selected_model,
            )
            .values_list("metadata__color", flat=True)
            .distinct()
            if current_selected_makes and current_selected_model
            else Offer.objects.filter(model__make__name__in=current_selected_makes)
            .values_list("metadata__color", flat=True)
            .distinct()
            if current_selected_makes
            else Offer.objects.filter(model__name__in=current_selected_model)
            .values_list("metadata__color", flat=True)
            .distinct()
            if current_selected_model
            else Offer.objects.values_list("metadata__color", flat=True).distinct()
        )

        get_friendly_color = lambda color: [  # noqa: E731
            value for k, value in OfferMetadata.COLOR_CHOICES if k == color
        ][0]

        color_objects = [Color(color=get_friendly_color(color)) for color in colors]
        return sorted(color_objects, key=lambda x: x.color)


class OfferComponentView(TemplateView):
    template_name = "all_offers.html"

    def __filter_data(
        self, offers: Any, filter: Dict[str, Any]
    ):  # todo change Any to BaseManager[Offer]
        if filter["value"] and filter["value"] != [""] and filter["value"] != ["Clear"]:
            offers = offers.filter(**{filter["key"]: filter["value"]})
        return offers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        base_queryset = Offer.objects.all()

        filter_params = self.request.GET
        filtered_offers = base_queryset

        get_unfriendly_color = lambda color: [  # noqa: E731
            k for k, value in OfferMetadata.COLOR_CHOICES if value == color
        ][0]

        filters = {
            "makes": {
                "key": "model__make__name__in",
                "value": filter_params.getlist("makes"),
            },
            "models": {
                "key": "model__name__in",
                "value": filter_params.getlist("models"),
            },
            "years": {
                "key": "production_year__in",
                "value": filter_params.getlist("years"),
            },
            "colors": {
                "key": "metadata__color__in",
                "value": [
                    get_unfriendly_color(c) for c in filter_params.getlist("colors")
                ],
            },
        }

        for key in filter_params.keys():
            filtered_offers = self.__filter_data(filtered_offers, filters.get(key))

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
