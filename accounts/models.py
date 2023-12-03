import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    id = models.UUIDField(
        _("user id"), primary_key=True, blank=False, default=uuid.uuid4
    )
    email = models.EmailField(_("email address"), blank=False, unique=True)
    phone_number = PhoneNumberField(blank=True, null=True, unique=True)

    def __str__(self):
        return self.email


class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(_("label"), blank=False)
    default_answers = ArrayField(models.CharField(max_length=256, blank=True))
    allow_custom_answer = models.BooleanField(
        max_length=512, default=True
    )  # allow user to type custom answer (max 512 chars)
    use_ratings = models.BooleanField(default=False)  # create poll with only 1-5 rating


class PollAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="answer")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="poll"
    )
    answer = models.CharField()
