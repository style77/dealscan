from django.urls import path

from billing import views

urlpatterns = [
    path("config/", views.stripe_config),
    path("checkout/", views.create_checkout_session, name="checkout"),
    path("plans/", views.plans, name="plans")
]
