"""Geography providers: countries, rivers, road signs."""

from memi_engine import CategoryProvider, register
from memi_engine import images

from memi.categories.countries import (
    ALL as COUNTRY_LIST,
    CAPITALS,
    CURRENCIES,
    CONTINENTS as COUNTRY_CONTINENTS,
    DIFFICULTY as COUNTRY_DIFFICULTY,
)
from memi.categories.rivers import (
    ALL as RIVER_LIST,
    CONTINENTS as RIVER_CONTINENTS,
    LOCATIONS as RIVER_LOCATIONS,
)
from memi.categories.roadsigns import (
    ALL as SIGN_LIST,
    COMMONS_FILES as SIGN_FILES,
    REGIONS as SIGN_REGIONS,
)


class CountryFlagsProvider(CategoryProvider):
    key = "geography:countries:flags"
    items = COUNTRY_LIST
    filters = {
        "continents": COUNTRY_CONTINENTS,
        "difficulty": COUNTRY_DIFFICULTY,
    }

    def get_image(self, item):
        result = images.get_wikipedia_image("Flag of " + item)
        if result and result.get("image"):
            result["name"] = item
            return result
        return None


class CountryCapitalsProvider(CategoryProvider):
    key = "geography:countries:capitals"
    items = COUNTRY_LIST
    filters = {
        "continents": COUNTRY_CONTINENTS,
        "difficulty": COUNTRY_DIFFICULTY,
    }

    def get_image(self, item):
        return images.get_country_shape(item)

    def get_clue(self, item):
        return item

    def get_tag(self, item):
        capital = CAPITALS.get(item, "Unknown")
        return capital


class CountryCurrenciesProvider(CategoryProvider):
    key = "geography:countries:currencies"
    items = COUNTRY_LIST
    filters = {
        "continents": COUNTRY_CONTINENTS,
        "difficulty": COUNTRY_DIFFICULTY,
    }

    def get_image(self, item):
        result = images.get_country_shape(item)
        if result:
            currency = CURRENCIES.get(item, "Unknown")
            currency_name = currency.split("(")[0].strip()
            result["clue"] = item
            result["name"] = currency_name
            if "(" in currency:
                result["tag"] = currency.split("(")[1].rstrip(")")
            img = images.get_wikipedia_image(currency_name)
            if img and img.get("image"):
                result["reveal_image"] = img["image"]
            return result
        return None

    def get_clue(self, item):
        return item


class CountryShapesProvider(CategoryProvider):
    key = "geography:countries:shapes"
    items = COUNTRY_LIST
    filters = {
        "continents": COUNTRY_CONTINENTS,
        "difficulty": COUNTRY_DIFFICULTY,
    }

    def get_image(self, item):
        return images.get_country_shape(item)


class RiversProvider(CategoryProvider):
    key = "geography:rivers"
    items = RIVER_LIST
    filters = {
        "continents": RIVER_CONTINENTS,
    }

    def get_image(self, item):
        return images.get_river_map(item)

    def get_tag(self, item):
        return RIVER_LOCATIONS.get(item)


class RoadSignsProvider(CategoryProvider):
    key = "geography:road signs"
    items = SIGN_LIST
    light_bg = True
    override_name = True

    def get_image(self, item):
        commons_file = SIGN_FILES.get(item)
        if commons_file:
            return images.get_commons_file_image(commons_file)
        return None

    def get_tag(self, item):
        region = SIGN_REGIONS.get(item)
        if region:
            return region
        return None


register(CountryFlagsProvider())
register(CountryCapitalsProvider())
register(CountryCurrenciesProvider())
register(CountryShapesProvider())
register(RiversProvider())
register(RoadSignsProvider())
