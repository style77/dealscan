import re
import time
from datetime import datetime
from typing import Callable, Dict, List, Union

from django.utils import timezone
from djmoney.money import Money

from crawler.formatters.formatter import BaseCrawler
from crawler.models import CarMake, CarModel, Offer, OfferMetadata

from . import constants


class Crawler(BaseCrawler):
    @staticmethod
    def _find_image_url(summary: str):
        pattern = r"https?://[^\s]+"

        urls = re.findall(pattern, summary)

        image_urls = [url for url in urls if "image" in url]

        if image_urls:
            return image_urls[0][:-1]

    def seperate_summary(self, entry: Dict):
        data = {}
        data["title"] = entry["title"]
        data["published_at"] = entry["published_parsed"]
        summary = entry["summary"]

        data["url"] = entry["links"][0]["href"]

        data["image_url"] = self._find_image_url(summary)

        summary_split = summary.split("<br />")
        data["description"] = "".join(summary_split[1:])
        split_data = [pair.split(":") for pair in summary_split[0].split(", ")]

        for _, pair in enumerate(split_data):
            try:
                key = pair[0].strip()
                val = pair[1].strip()
            except IndexError:
                key = pair[0].strip()
                val = ""

            # if key in ("Spalanie W Mieście", "Spalanie Poza Miastem") and split_data[i+1][1] == "":
            data[key] = val

        price_split = data["Cena"].split(" ")
        data["price"] = float("".join(price_split[:-1]).replace(" ", ""))
        data["currency"] = price_split[-1]
        return data

    @staticmethod
    def _to_bool(val: str) -> bool:
        match val:
            case "Nie":
                return False
            case "Tak":
                return True
            case _:
                return False  # Doesn't matter

    @staticmethod
    def _get_fuel_consumption(val: str) -> float:
        consumption_split = val.split(" ")
        return float(consumption_split[0].replace(",", "."))

    @staticmethod
    def _get_map_option(
        data, key, converter: Union[dict, Callable], default_value=None
    ):
        if isinstance(converter, dict):
            return converter.get(data[key]) if data.get(key) else default_value
        elif callable(converter):
            return converter(data[key]) if data.get(key) else default_value

    def format_data(self, data: Dict) -> Offer:
        # Since different pages save makes and models in different ways
        # we need to create make if it doesn't exist
        # TODO: Find a way to prevent saving same make multiple times
        make, _ = CarMake.objects.get_or_create(name=data["Marka pojazdu"])
        model, _ = CarModel.objects.get_or_create(name=data["Model pojazdu"], make=make)

        out_of_town_consumption = (
            self._get_fuel_consumption(data["Spalanie Poza Miastem"])
            if data.get("Spalanie Poza Miastem")
            else None
        )
        in_of_town_consumption = (
            self._get_fuel_consumption(data["Spalanie W Mieście"])
            if data.get("Spalanie W Mieście")
            else None
        )

        first_registration_date = None
        if data.get("Data pierwszej rejestracji w historii pojazdu"):
            frd = data["Data pierwszej rejestracji w historii pojazdu"]
            frd_split = frd.split(" ")
            if len(frd_split) == 2:
                frd_split.insert(0, "1")
            day = frd_split[0]
            month = constants.MONTH_TRANSLATION_MAP.get(frd_split[1].lower(), 2)
            year = frd_split[2]
            frd = f"{day} {month} {year}"
            first_registration_date = timezone.make_aware(
                datetime.strptime(frd, "%d %m %Y"), timezone.get_current_timezone()
            )

        doors_count = int(data["Liczba drzwi"]) if data.get("Liczba drzwi") else None

        metadata = OfferMetadata(
            out_of_town_consumption=out_of_town_consumption,
            in_town_consumption=in_of_town_consumption,
            power=int(data["Moc"].replace(" KM", "").replace(" ", "")),
            co2_emission=int(data["Emisja CO2"].replace(" g/km", ""))
            if data.get("Emisja CO2")
            else None,
            doors_count=doors_count,
            seats_count=self._get_map_option(data, "Liczba miejsc", int),
            color=constants.COLOR_CHOICES_MAP.get(data["Kolor"], "other"),
            color_type=self._get_map_option(
                data, "Rodzaj koloru", constants.FINISH_CHOICES_MAP
            ),
            origin_country=self._get_map_option(
                data, "Kraj pochodzenia", constants.ORIGIN_COUNTRIES_MAP
            ),
            first_registration_date=first_registration_date,
            registration_number=data.get("Numer rejestracyjny pojazdu"),
            first_owner=self._get_map_option(
                data, "Pierwszy właściciel (od nowości)", self._to_bool
            ),
            never_damaged=self._get_map_option(
                data, "Bezwypadkowy", self._to_bool, None
            ),
            left_steering_wheel=not self._get_map_option(
                data, "Kierownica po prawej (Anglik)", self._to_bool, None
            ),
            features=None,
        )

        displacement = (
            int(data["Pojemność skokowa"].replace(" cm3", "").replace(" ", ""))
            if data.get("Pojemność skokowa")
            else None
        )

        offer = Offer(
            id=data["url"].split("/")[-1],
            source=self.source,
            metadata=metadata,
            title=data["title"],
            url=data["url"],
            publication_date=timezone.make_aware(
                datetime.fromtimestamp(time.mktime(data["published_at"])),
                timezone.get_current_timezone(),
            ),
            image_url=data["image_url"],
            description=data["description"],
            model=model,
            trim=data.get("Wersja"),
            generation=data.get("Generacja"),
            production_year=int(data["Rok produkcji"]),
            mileage=int(data["Przebieg"].replace(" km", "").replace(" ", "")),
            displacement=displacement,
            fuel=constants.FUEL_CHOICES_MAP.get(data["Rodzaj paliwa"], "other"),
            transmission=constants.TRANSMISSION_CHOICES_MAP[
                data["Skrzynia biegów"]
            ],  # 162
            drive=data.get("Napęd"),
            damaged=self._to_bool(data["Uszkodzony"])
            if data.get("Uszkodzony")
            else None,
            body=constants.BODY_CHOICES_MAP.get(data["Typ nadwozia"], "other"),
            price=Money(float(data["price"]), data["currency"]),
            VIN=data.get("VIN"),
            is_imported=self._to_bool(data["Importowany"]),
        )

        return offer

    def crawl_offers(self) -> List[Offer]:
        feed_data = self._parse_feed()
        offers: List[Offer] = []
        for entry in feed_data["entries"]:
            try:
                data = self.seperate_summary(entry)
                if Offer.objects.filter(url=data["url"]).exists():
                    break
                offer = self.format_data(data)
                offers.append(offer)
            except Exception:
                continue

        return offers
