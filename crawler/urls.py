from django.urls import path

from crawler.views import billing_view, dashboard_view, offers_view, all_offers_view

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/billing/", billing_view, name="dashboard_billing"),
    path("dashboard/offers/", offers_view, name="dashboard_offers"),
    path("dashboard/offers/all/", all_offers_view, name="dashboard_all_offers"),
]
