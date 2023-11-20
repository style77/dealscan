from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

import stripe


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def plans(request):
    if request.method == "GET":
        all_products = stripe.Product.list(active=True, expand=["data.price"])

        products = []
        for product in all_products:
            prices = {}
            for price in stripe.Price.list(product=product.id).data:
                prices[price.recurring.interval] = {
                    "price_id": price.id,
                    "unit_amount": price.unit_amount,
                    "currency": price.currency,
                    "trial_period_days": price.recurring.trial_period_days,
                }

            products.append(
                {
                    "product_id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "features": product.features,
                    "prices": prices,
                }
            )

        return JsonResponse(products, safe=False)


LOGIN_URL = reverse_lazy("account_login")


@csrf_exempt
@login_required(login_url=LOGIN_URL)
def create_checkout_session(request):
    if request.method == "GET":
        domain_url = "http://localhost:8000/"
        price_id = (
            settings.STRIPE_PRICE_ID_YEAR
            if request.GET.get("recurring", None) == "year"
            else settings.STRIPE_PRICE_ID_MONTH
        )
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id,
                success_url=domain_url + request.GET.get("success_url", "success?session_id={CHECKOUT_SESSION_ID}"),
                cancel_url=domain_url + request.GET.get("cancel_url", "cancel/"),
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
            )
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})
