import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from djstripe.models import Customer


class User(AbstractUser):
    id = models.UUIDField(
        _("user id"), primary_key=True, blank=False, default=uuid.uuid4
    )
    email = models.EmailField(_("email address"), blank=False, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.email

    @property
    def stripe_user(self):
        stripe_user, _ = Customer.get_or_create(subscriber=self)
        return stripe_user
