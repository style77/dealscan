import stripe
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from allauth.account.signals import email_confirmed
from django.shortcuts import get_object_or_404


User = get_user_model()


class StripeUser(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="stripe_user"
    )
    customer_id = models.CharField(max_length=128, null=False)
    subscription_id = models.CharField(max_length=255, null=True)


@receiver(email_confirmed)
def create_stripe_customer(sender, request, email_address, **kwargs):
    user = get_object_or_404(User, email=email_address)
    if request.user.is_anonymous:
        return

    customer = stripe.Customer.create(email=user.email)
    StripeUser.objects.create(user=user, customer_id=customer.id)
