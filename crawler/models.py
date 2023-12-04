from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from simple_history.models import HistoricalRecords


class Source(models.Model):  # type: ignore[django-manager-missing]
    # RSS feed to be crawled
    name = models.CharField(
        _("name"), max_length=255
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


class CarModel(models.Model):  # type: ignore[django-manager-missing]
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

    out_of_town_consumption = models.DecimalField(
        _("out of town fuel consumption"),
        decimal_places=1,
        max_digits=3,
        blank=True,
        null=True,
    )
    in_town_consumption = models.DecimalField(
        _("in town fuel consumption"),
        decimal_places=1,
        max_digits=3,
        blank=True,
        null=True,
    )

    power = models.PositiveSmallIntegerField(_("engine power"))
    co2_emission = models.PositiveSmallIntegerField(
        _("co2 emission"), blank=True, null=True
    )
    doors_count = models.PositiveSmallIntegerField(_("doors count"), blank=True, null=True)
    seats_count = models.PositiveSmallIntegerField(
        _("seats count"), blank=True, null=True
    )

    color = models.CharField(_("vehicle color"), choices=COLOR_CHOICES)
    color_type = models.CharField(
        _("vehicle color type"), choices=FINISH_CHOICES, null=True, blank=True
    )

    origin_country = CountryField(_("origin country"), null=True, blank=True)

    first_registration_date = models.DateTimeField(
        _("first registration date"), blank=True, null=True
    )
    registration_number = models.CharField(
        _("registration number"), max_length=24, blank=True, null=True
    )
    first_owner = models.BooleanField(_("first owner"), null=True, blank=True)

    never_damaged = models.BooleanField(
        _("have vehicle been ever damaged"), null=True, blank=True
    )

    features = models.JSONField(_("car features"), null=True, blank=True)

    left_steering_wheel = models.BooleanField(
        _("does vehicle have steering wheel on the left side"), null=True, blank=True
    )


class Offer(models.Model):  # type: ignore[django-manager-missing]
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

    id = models.SlugField(primary_key=True, max_length=512, unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="offers")
    metadata = models.OneToOneField(OfferMetadata, on_delete=models.CASCADE)

    title = models.CharField(_("title"), max_length=1024)
    url = models.URLField(_("url"), unique=True)
    image_url = models.URLField(_("image_url"), unique=True, null=True, blank=True, max_length=2048)
    publication_date = models.DateTimeField(
        _("publication_date"),
    )

    description = models.CharField(_("description"))

    model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="offers")
    trim = models.CharField(_("trim"), blank=True, null=True)
    generation = models.CharField(_("generation"), blank=True, null=True)

    production_year = models.PositiveSmallIntegerField(_("production year"))
    mileage = models.PositiveIntegerField(_("mileage"))
    displacement = models.PositiveSmallIntegerField(_("engine displacement"), blank=True, null=True)

    fuel = models.CharField(_("fuel type"), choices=FUEL_CHOICES)
    transmission = models.CharField(_("transmission"), choices=TRANSMISSION_CHOICES)
    drive = models.CharField(_("drive"), null=True, blank=True)
    damaged = models.BooleanField(_("is vehicle damaged"), blank=True, null=True)
    body = models.CharField(_("body type"), choices=BODY_CHOICES)

    price = MoneyField(
        _("price"), max_digits=12, decimal_places=2, default_currency="PLN"
    )

    VIN = models.CharField(_("VIN number"), blank=True, null=True)
    is_imported = models.BooleanField(_("is vehicle imported"))
