from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from crawler.models import CarMake, CarModel, Offer, OfferMetadata, Source
from dealscan.sites import unfold_admin_site


@admin.register(Source, site=unfold_admin_site)
class SourceAdmin(ModelAdmin):
    def image_tag(self, obj: Source):
        return format_html('<img src="{}" />'.format(obj.image_url))

    image_tag.short_description = ""  # type: ignore

    list_display = ["image_tag", "name", "description", "last_polled", "active"]


@admin.register(Offer, site=unfold_admin_site)
class OfferAdmin(ModelAdmin):
    pass


@admin.register(OfferMetadata, site=unfold_admin_site)
class OfferMetadataAdmin(ModelAdmin):
    pass


@admin.register(CarMake, site=unfold_admin_site)
class CarMakeAdmin(ModelAdmin):
    search_fields = ["name"]


@admin.register(CarModel, site=unfold_admin_site)
class CarModelAdmin(ModelAdmin):
    list_display = ["name", "make"]
    search_fields = ["name", "make__name"]
    ordering = ["make"]
