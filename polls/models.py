from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class Poll(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.CharField(_("label"), blank=False, max_length=256)
    description = models.CharField(
        _("description"), max_length=512, blank=True, null=True
    )
    default_answers = ArrayField(models.CharField(max_length=256, blank=True))
    allow_custom_answer = models.BooleanField(
        max_length=512, default=True
    )  # allow user to type custom answer (max 512 chars)
    use_ratings = models.BooleanField(default=False)  # create poll with only 1-5 rating

    def clean(self):
        if self.default_answers and self.use_ratings and self.allow_custom_answer:
            raise ValidationError(
                _(
                    "Poll cannot have default answers and allow custom answers with ratings enabled."
                )
            )
        super().clean()


class PollAnswer(models.Model):
    id = models.BigAutoField(primary_key=True)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="answer")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="poll",
    )
    answer = models.CharField()

    class Meta:
        unique_together = ("user", "poll")
