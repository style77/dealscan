from django.contrib import admin
from unfold.admin import ModelAdmin

from crawler.models import CarMake, CarModel, Offer, OfferMetadata, Source
from dealscan.sites import unfold_admin_site


@admin.register(Source, site=unfold_admin_site)
class SourceAdmin(ModelAdmin):
    pass


@admin.register(Offer, site=unfold_admin_site)
class OfferAdmin(ModelAdmin):
    pass


@admin.register(OfferMetadata, site=unfold_admin_site)
class OfferMetadataAdmin(ModelAdmin):
    pass


@admin.register(CarMake, site=unfold_admin_site)
class CarMakeAdmin(ModelAdmin):
    pass


@admin.register(CarModel, site=unfold_admin_site)
class CarModelAdmin(ModelAdmin):
    pass
