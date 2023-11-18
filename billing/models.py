from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class StripeUser(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="stripe_user"
    )
    customer_id = models.CharField(max_length=128, null=False)
