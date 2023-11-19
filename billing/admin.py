from django.contrib import admin
from unfold.admin import ModelAdmin

from billing.models import StripeUser


@admin.register(StripeUser)
class StripeUserAdmin(ModelAdmin):
    ...
