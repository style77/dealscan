from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords


class Source(models.Model):
    # RSS feed to be crawled
    name = models.CharField(
        _("name"), max_length=255, blank=True, null=True
    )  # this is also going to be formatter name
    site_url = models.URLField(_("site url"), max_length=255, blank=True, null=True)
    feed_url = models.URLField(_("feed url"), max_length=512)
    image_url = models.URLField(_("image url"), max_length=1024, blank=True, null=True)

    description = models.CharField(_("description"), null=True, blank=True)

    last_polled = models.DateTimeField(_("last polled"), blank=True, null=True)

    interval = models.PositiveIntegerField(
        _("interval"), default=500
    )  # interval in seconds
    active = models.BooleanField(_("active"), default=True)

    history = HistoricalRecords()

    def __str__(self) -> str:
        return self.name.capitalize()


class CarMake(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("make", "name")

    def __str__(self) -> str:
        return self.name


class OfferMetadata(models.Model):
    COLOR_CHOICES = [
        ("beige", _("Beige")),
        ("white", _("White")),
        ("sky-blue", _("Sky Blue")),
        ("maroon", _("Maroon")),
        ("brown", _("Brown")),
        ("black", _("Black")),
        ("red", _("Red")),
        ("purple", _("Purple")),
        ("navy-blue", _("Navy Blue")),
        ("other", _("Other Color")),
        ("blue", _("Blue")),
        ("orange", _("Orange")),
        ("silver", _("Silver")),
        ("gray", _("Gray")),
        ("green", _("Green")),
        ("gold", _("Gold")),
        ("yellow", _("Yellow")),
    ]

    FINISH_CHOICES = [
        ("matte", _("Matte")),
        ("metallic", _("Metallic")),
        ("pearl", _("Pearl")),
    ]

    out_of_town_consumption = models.PositiveSmallIntegerField(
        _("out of town fuel consumption"), blank=True, null=True
    )
    in_town_consumption = models.PositiveSmallIntegerField(
        _("in town fuel consumption"), blank=True, null=True
    )

    power = models.PositiveSmallIntegerField(_("engine power"))
    co2_emission = models.PositiveSmallIntegerField(
        _("co2 emission"), blank=True, null=True
    )
    doors_count = models.PositiveSmallIntegerField(_("doors count"))
    seats_count = models.PositiveSmallIntegerField(_("seats count"))

    color = models.CharField(_("vehicle color"), choices=COLOR_CHOICES)
    color_type = models.CharField(_("vehicle color type"), choices=FINISH_CHOICES)

    origin_country = CountryField(_("origin country"))

    first_registration_date = models.DateTimeField(
        _("first registration date"), blank=True, null=True
    )
    registration_number = models.CharField(
        _("registration number"), max_length=7, blank=True, null=True
    )
    first_owner = models.BooleanField(_("first owner"))

    never_damaged = models.BooleanField(_("have vehicle been ever damaged"))

    features = models.JSONField(_("car features"))

    radio = models.BooleanField(_("does vehicle have radio"))
    left_steering_wheel = models.BooleanField(
        _("does vehicle have steering wheel on the left side")
    )

    from_authorized_dealer = models.BooleanField(_("is vehicle from authorized dealer"))
    has_registration_number = models.BooleanField(
        _("does vehicle have registration number")
    )


class Offer(models.Model):
    FUEL_CHOICES = (
        ("diesel", _("Diesel")),
        ("petrol", _("Petrol")),
        ("hybrid", _("Hybrid")),
        ("lpg", _("LPG")),
        ("cng", _("CNG")),
        ("electric", _("Electric")),
        ("other", _("Other")),
    )
    TRANSMISSION_CHOICES = (("manual", _("Manual")), ("automatic", _("Automatic")))
    BODY_CHOICES = (
        ("suv", _("SUV")),
        ("sedan", _("Sedan")),
        ("minivan", _("Minivan")),
        ("compact", _("Compact")),
        ("combi", _("Combi")),
        ("cabrio", _("Cabrio")),
        ("coupe", _("Coupe")),
        ("other", _("Other")),
    )

    id = models.SlugField(primary_key=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="offers")
    metadata = models.OneToOneField(OfferMetadata, on_delete=models.CASCADE)

    title = models.CharField(_("title"), max_length=1024)
    url = models.URLField(_("url"), unique=True)
    publication_date = models.DateTimeField(
        _("publication_date"),
    )

    description = models.CharField(_("description"))

    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="offers")
    trim = models.CharField(_("trim"), blank=True, null=True)
    generation = models.CharField(_("generation"), blank=True, null=True)

    production_year = models.PositiveSmallIntegerField(_("production year"))
    mileage = models.PositiveIntegerField(_("mileage"))
    displacement = models.PositiveSmallIntegerField(_("engine displacement"))

    fuel = models.CharField(_("fuel type"), choices=FUEL_CHOICES)
    transmission = models.CharField(_("transmission"), choices=TRANSMISSION_CHOICES)
    drive = models.CharField(_("drive"))
    damaged = models.BooleanField(_("is vehicle damaged"))
    body = models.CharField(_("body type"), choices=BODY_CHOICES)

    price = MoneyField(
        _("price"), max_digits=12, decimal_places=2, default_currency="PLN"
    )

    VIN = models.CharField(_("VIN number"), blank=True, null=True)
    is_imported = models.BooleanField(_("is vehicle imported"))
