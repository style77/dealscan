from django.urls import path

from crawler.views import billing_view, dashboard_view

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard"),
    path("dashboard/billing/", billing_view, name="dashboard_billing"),
]
