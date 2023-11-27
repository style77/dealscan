from django.urls import path
from crawler.views import dashboard_view

urlpatterns = [
    path("dashboard/", dashboard_view, name="dashboard")
]
