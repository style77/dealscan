import functools
from django.shortcuts import redirect
from djstripe.models import Subscription, Customer
from djstripe.enums import SubscriptionStatus


def subscription_required(function):
    @functools.wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(subscriber=request.user)
            if not customer.exists():
                return redirect("dashboard_billing")
            
            customer = customer.first()

            if Subscription.objects.filter(
                customer=customer, status=SubscriptionStatus.active
            ).exists():
                return function(request, *args, **kwargs)
            else:
                return redirect("dashboard_billing")
        else:
            return redirect("account_login")

    return wrap
