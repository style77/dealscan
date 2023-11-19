import time
from datetime import datetime
from typing import Dict, List

from djmoney.money import Money
from django.utils import timezone

from crawler.formatters.formatter import BaseCrawler
from crawler.models import CarMake, CarModel, Offer, OfferMetadata


class Crawler(BaseCrawler):
    TRANSMISSION_CHOICES_MAP = {
        "Automatyczna": "automatic",
        "Manualna": "manual",
    }
    FUEL_CHOICES_MAP = {
        "Benzyna": "petrol",
        "Diesel": "diesel",
        "Benzyna+LPG": "lpg",
        "Benzyna+CNG": "cng",
        "Diesel": "diesel",
        "Elektryczny": "electric",
        "Hybrydowy": "hybrid",
    }
    BODY_CHOICES_MAP = {
        "Minivan": "minivan",
        "Sedan": "sedan",
        "SUV": "suv",
        "Kombi": "combi",
        "Kompakt": "compact",
        "Coupe": "coupe",
        "Kabriolet": "cabrio",
    }
    COLOR_CHOICES_MAP = {
        "Beżowy": "beige",
        "Biały": "white",
        "Błękitny": "sky-blue",
        "Kasztanowy": "maroon",
        "Brązowy": "brown",
        "Czarny": "black",
        "Czerwony": "red",
        "Fioletowy": "purple",
        "Granatowy": "navy-blue",
        "Niebieski": "blue",
        "Pomarańczowy": "orange",
        "Srebrny": "silver",
        "Szary": "gray",
        "Zielony": "green",
        "Złoty": "gold",
        "Żółty": "yellow",
    }
    FINISH_CHOICES_MAP = {
        "Matowy": "matte",
        "Metalik": "metallic",
        "Perłowy": "pearl",
    }
    ORIGIN_COUNTRIES_MAP = {
        "Austria": "AT",
        "Belgia": "BE",
        "Białoruś": "BY",
        "Bułgaria": "BG",
        "Chorwacja": "HR",
        "Czechy": "CZ",
        "Dania": "DK",
        "Estonia": "EE",
        "Finlandia": "FI",
        "Francja": "FR",
        "Grecja": "GR",
        "Hiszpania": "ES",
        "Holandia": "NL",
        "Irlandia": "IE",
        "Islandia": "IS",
        "Japonia": "JP",
        "Kanada": "CA",
        "Korea": "KR",
        "Liechtenstein": "LI",
        "Litwa": "LT",
        "Luksemburg": "LU",
        "Łotwa": "LV",
        "Monako": "MC",
        "Niemcy": "DE",
        "Norwegia": "NO",
        "Polska": "PL",
        "Rosja": "RU",
        "Rumunia": "RO",
        "Słowacja": "SK",
        "Słowenia": "SI",
        "Stany Zjednoczone": "US",
        "Szwajcaria": "CH",
        "Szwecja": "SE",
        "Turcja": "TR",
        "Ukraina": "UA",
        "Węgry": "HU",
        "Wielka Brytania": "GB",
        "Włochy": "IT",
    }
    MONTH_TRANSLATION_MAP = {
        "styczeń": 1,
        "luty": 2,
        "marzec": 3,
        "kwiecień": 4,
        "maj": 5,
        "czerwiec": 6,
        "lipiec": 7,
        "sierpień": 8,
        "wrzesień": 9,
        "październik": 10,
        "listopad": 11,
        "grudzień": 12,
    }

    def seperate_summary(self, entry: Dict):
        data = {}
        data["title"] = entry["title"]
        data["published_at"] = entry["published_parsed"]
        summary = entry["summary"]
        data["url"] = entry["links"][0]["href"]

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
        return float(consumption_split[0])

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
            day = frd_split[0]
            month = self.MONTH_TRANSLATION_MAP.get(frd_split[1].lower(), 2)
            year = frd_split[2]
            frd = f"{day} {month} {year}"
            first_registration_date = timezone.make_aware(
                datetime.strptime(frd, "%d %m %Y"), timezone.get_current_timezone()
            )

        metadata = OfferMetadata(
            out_of_town_consumption=out_of_town_consumption,
            in_town_consumption=in_of_town_consumption,
            power=int(data["Moc"].replace(" KM", "")),
            co2_emission=int(data["Emisja CO2"].replace(" g/km", ""))
            if data.get("Emisja CO2")
            else None,
            doors_count=int(data["Liczba drzwi"]),
            seats_count=int(data["Liczba miejsc"])
            if data.get("Liczba miejsc")
            else None,
            color=self.COLOR_CHOICES_MAP.get(data["Kolor"], "other"),
            color_type=self.FINISH_CHOICES_MAP.get(data["Rodzaj koloru"])
            if data.get("Rodzaj koloru")
            else None,
            origin_country=self.ORIGIN_COUNTRIES_MAP.get(data["Kraj pochodzenia"])
            if data.get("Kraj pochodzenia")
            else None,  # type: ignore
            first_registration_date=first_registration_date,
            registration_number=data.get("Numer rejestracyjny pojazdu"),
            first_owner=self._to_bool(data["Pierwszy właściciel (od nowości)"])
            if data.get("Pierwszy właściciel (od nowości)")
            else None,
            never_damaged=self._to_bool(data["Bezwypadkowy"])
            if data.get("Bezwypadkowy")
            else None,
            left_steering_wheel=not self._to_bool(data["Kierownica po prawej (Anglik)"])
            if data.get("Kierownica po prawej (Anglik)")
            else None,
            features=None,
        )

        offer = Offer(
            id=data["url"].split("/")[-1],
            source=self.source,
            metadata=metadata,
            title=data["title"],
            url=data["url"],
            publication_date=timezone.make_aware(datetime.fromtimestamp(time.mktime(data["published_at"])), timezone.get_current_timezone()),
            description=data["description"],
            model=model,
            trim=data.get("Wersja"),
            generation=data.get("Generacja"),
            production_year=int(data["Rok produkcji"]),
            mileage=int(data["Przebieg"].replace(" km", "").replace(" ", "")),
            displacement=int(
                data["Pojemność skokowa"].replace(" cm3", "").replace(" ", "")
            ),
            fuel=self.FUEL_CHOICES_MAP.get(data["Rodzaj paliwa"], "other"),
            transmission=self.TRANSMISSION_CHOICES_MAP[data["Skrzynia biegów"]],  # 162
            drive=data.get("Napęd"),
            damaged=self._to_bool(data["Uszkodzony"])
            if data.get("Uszkodzony")
            else None,
            body=self.BODY_CHOICES_MAP.get(data["Typ nadwozia"], "other"),
            price=Money(float(data["price"]), data["currency"]),
            VIN=data.get("VIN"),
            is_imported=self._to_bool(data["Importowany"]),
        )

        return offer

    def crawl_offers(self) -> List[Offer]:
        feed_data = self._parse_feed()
        offers: List[Offer] = []
        for entry in feed_data["entries"]:
            data = self.seperate_summary(entry)
            offer = self.format_data(data)
            offers.append(offer)

        return offers
