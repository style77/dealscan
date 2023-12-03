from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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
