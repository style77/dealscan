import stripe
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class StripeUser(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="stripe_user"
    )
    customer_id = models.CharField(max_length=128, null=False)
    subscription_id = models.CharField(max_length=255, null=True)


@receiver(post_save, sender=User, dispatch_uid="create_stripe_customer")
def create_stripe_customer(sender, instance: User, **kwargs):
    customer = stripe.Customer.create(email=instance.email)
    StripeUser.objects.create(user=instance, customer_id=customer.id)