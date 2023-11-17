import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(
        _("user id"), primary_key=True, blank=False, default=uuid.uuid4
    )
    email = models.EmailField(_("email address"), blank=False, unique=True)

    def __str__(self):
        return self.email
