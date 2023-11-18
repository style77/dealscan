from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from dealscan.sites import unfold_admin_site
from crawler.models import Source, Offer, OfferMetadata, CarMake, CarModel


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
