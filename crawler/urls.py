from django.urls import path, include

from crawler.views import all_offers_view, billing_view, dashboard_view, offers_view
from crawler.decorators import subscription_required

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/billing/", billing_view, name="dashboard_billing"),
    path(
        "dashboard/offers/", subscription_required(offers_view), name="dashboard_offers"
    ),
    path(
        "dashboard/offers/all/",
        subscription_required(all_offers_view),
        name="dashboard_all_offers",
    ),
    path("payments/", include("djstripe.urls", namespace="djstripe")),
]
