from django.contrib import admin
from unfold.admin import ModelAdmin
from dealscan.sites import unfold_admin_site
from .models import Poll, PollAnswer


@admin.register(Poll, site=unfold_admin_site)
class PollAdmin(ModelAdmin):
    ...


@admin.register(PollAnswer, site=unfold_admin_site)
class PollAnswerAdmin(ModelAdmin):
    ...
