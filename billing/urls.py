from django.urls import path

from billing import views

urlpatterns = [
    path("config/", views.stripe_config)
]
