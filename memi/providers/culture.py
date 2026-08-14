"""Culture providers: monuments, paintings, characters, cinema, music, sports, brands."""

from typing import ClassVar

from memi_engine import CategoryProvider, images, register

from memi.categories.albums import (
    ALL as ALBUM_LIST,
    ARTISTS as ALBUM_ARTISTS,
    MBIDS as ALBUM_MBIDS,
    YEARS as ALBUM_YEARS,
)
from memi.categories.brands import (
    AIRLINES_NAMES,
    ALL_NAMES as BRAND_ALL_NAMES,
    AUTOMOTIVE_NAMES,
    BRAND_TAGS,
    FASHION_NAMES,
    FOOD_AND_DRINK_NAMES,
    TECH_NAMES,
)
from memi.categories.characters import (
    ALL as CHAR_ALL,
    ANIME,
    DC,
    DISNEY,
    HARRY_POTTER,
    LORD_OF_THE_RINGS,
    MARVEL,
    STAR_WARS,
)
from memi.categories.directors import ALL as DIRECTOR_LIST
from memi.categories.instruments import (
    ALL as INSTRUMENT_LIST,
    FAMILIES as INSTRUMENT_FAMILIES,
)
from memi.categories.logos import LOGOS
from memi.categories.monuments import (
    ALL as MONUMENT_LIST,
    CONTINENTS as MONUMENT_CONTINENTS,
    DIFFICULTY as MONUMENT_DIFFICULTY,
    LOCATIONS as MONUMENT_LOCATIONS,
)
from memi.categories.movies import ALL as MOVIE_LIST, YEARS as MOVIE_YEARS
from memi.categories.paintings import (
    MOVEMENT_PERIODS,
    MOVEMENTS,
    PAINTERS,
    PAINTING_INFO,
    PAINTINGS,
)
from memi.categories.people import ACTORS
from memi.categories.sports import (
    EUROS_ALL,
    FOOTBALL_CLUBS_ALL,
    IMAGE_FILES as SPORT_IMAGE_FILES,
    OLYMPICS_ALL,
    SPORTS_ALL,
    SUMMER_OLYMPICS_ALL,
    TAGS as SPORT_TAGS,
    WIKIPEDIA as SPORT_WIKIPEDIA,
    WINTER_OLYMPICS_ALL,
    WORLD_CUPS_ALL,
)
from memi.categories.tvshows import ALL as TV_LIST, YEARS as TV_YEARS

# -- Monuments --

class MonumentsProvider(CategoryProvider):
    key = "culture:art:monuments"
    items = MONUMENT_LIST
    filters: ClassVar[dict[str, dict[str, list[str]]]] = {
        "continents": MONUMENT_CONTINENTS,
        "difficulty": MONUMENT_DIFFICULTY,
    }

    def get_tag(self, item):
        return MONUMENT_LOCATIONS.get(item)


# -- Paintings --

class PaintingMovementsProvider(CategoryProvider):
    key = "culture:art:paintings:movements"
    items = MOVEMENTS

    def get_tag(self, item):
        return MOVEMENT_PERIODS.get(item)


class PaintersProvider(CategoryProvider):
    key = "culture:art:paintings:painters"
    items = PAINTERS


class PaintingsProvider(CategoryProvider):
    key = "culture:art:paintings:paintings"
    items = PAINTINGS

    def get_tag(self, item):
        return PAINTING_INFO.get(item)


# -- Characters --

FANDOM_WIKIS = {
    "culture:cinema:characters:star wars": "starwars",
    "culture:cinema:characters:lord of the rings": "lotr",
    "culture:cinema:characters:harry potter": "harrypotter",
    "culture:cinema:characters:disney": "disney",
    "culture:cinema:characters:marvel": "marvel",
    "culture:cinema:characters:dc": "dc",
    "culture:cinema:characters:anime": None,
    "culture:cinema:characters:all": None,
}


def _make_character_provider(key, item_list):
    wiki = FANDOM_WIKIS.get(key)

    class CharProvider(CategoryProvider):
        pass

    CharProvider.key = key
    CharProvider.items = item_list

    if wiki:
        def get_image(self, item):
            result = images.get_fandom_image(item, wiki)
            if result and result.get("image"):
                return result
            return images.get_wikipedia_image(item)
        CharProvider.get_image = get_image
    else:
        # For anime and all: no fandom wiki, just wikipedia
        pass

    return CharProvider


CharAllProvider = _make_character_provider("culture:cinema:characters:all", CHAR_ALL)
CharStarWarsProvider = _make_character_provider("culture:cinema:characters:star wars", STAR_WARS)
CharLotrProvider = _make_character_provider("culture:cinema:characters:lord of the rings", LORD_OF_THE_RINGS)
CharHPProvider = _make_character_provider("culture:cinema:characters:harry potter", HARRY_POTTER)
CharDisneyProvider = _make_character_provider("culture:cinema:characters:disney", DISNEY)
CharMarvelProvider = _make_character_provider("culture:cinema:characters:marvel", MARVEL)
CharDCProvider = _make_character_provider("culture:cinema:characters:dc", DC)
CharAnimeProvider = _make_character_provider("culture:cinema:characters:anime", ANIME)


# -- Actors & Directors --

class ActorsProvider(CategoryProvider):
    key = "culture:cinema:actors"
    items = ACTORS

    def get_tag(self, item):
        desc = images.get_wikipedia_description(item)
        if desc:
            desc = desc.replace("(born ", "(").replace("(", "").replace(")", "")
            return desc
        return None


class DirectorsProvider(CategoryProvider):
    key = "culture:cinema:directors"
    items = DIRECTOR_LIST

    def get_tag(self, item):
        desc = images.get_wikipedia_description(item)
        if desc:
            desc = desc.replace("(born ", "(").replace("(", "").replace(")", "")
            return desc
        return None


# -- Movies --

class MoviePostersProvider(CategoryProvider):
    key = "culture:cinema:movies:posters"
    items = MOVIE_LIST
    footers: ClassVar[list[str]] = ["tmdb"]

    def get_image(self, item):
        result = images.get_tmdb_image(item, "poster")
        if result and result.get("image"):
            return result
        return images.get_wikipedia_image(item)

    def get_tag(self, item):
        return MOVIE_YEARS.get(item)


class MovieScenesProvider(CategoryProvider):
    key = "culture:cinema:movies:scenes"
    items = MOVIE_LIST
    footers: ClassVar[list[str]] = ["tmdb"]

    def get_image(self, item):
        result = images.get_tmdb_image(item, "backdrop")
        if result and result.get("image"):
            return result
        return images.get_wikipedia_image(item)

    def get_tag(self, item):
        return MOVIE_YEARS.get(item)


# -- TV Shows --

class TVShowsProvider(CategoryProvider):
    key = "culture:cinema:tv shows:scenes"
    items = TV_LIST
    footers: ClassVar[list[str]] = ["tmdb"]

    def get_image(self, item):
        result = images.get_tmdb_tv_image(item, "backdrop")
        if result and result.get("image"):
            return result
        return images.get_wikipedia_image(item)

    def get_tag(self, item):
        return TV_YEARS.get(item)


# -- Albums --

class AlbumsProvider(CategoryProvider):
    key = "culture:music:albums"
    items = ALBUM_LIST
    footers: ClassVar[list[str]] = ["musicbrainz"]

    def get_image(self, item):
        mbid = ALBUM_MBIDS.get(item)
        return images.get_album_cover(item, mbid)

    def get_tag(self, item):
        artist = ALBUM_ARTISTS.get(item)
        year = ALBUM_YEARS.get(item, "")
        if artist:
            return f"{artist} {year}"
        return None


# -- Instruments --

class InstrumentsProvider(CategoryProvider):
    key = "culture:music:instruments"
    items = INSTRUMENT_LIST
    filters: ClassVar[dict[str, dict[str, list[str]]]] = {
        "families": INSTRUMENT_FAMILIES,
    }


# -- Sports --

def _make_sports_provider(key, item_list):
    class SportsProvider(CategoryProvider):
        light_bg = True
        override_name = True

        def get_image(self, item):
            if item in LOGOS:
                return {"name": item, "image": LOGOS[item]}
            image_file = SPORT_IMAGE_FILES.get(item)
            if image_file:
                result = images.get_wikipedia_file_image(image_file)
                if result and result.get("image"):
                    return result
            wiki = SPORT_WIKIPEDIA.get(item, item)
            return images.get_wikipedia_image(wiki)

        def get_tag(self, item):
            return SPORT_TAGS.get(item)

    SportsProvider.key = key
    SportsProvider.items = item_list
    return SportsProvider


SportsAllProvider = _make_sports_provider("culture:sports:sports", SPORTS_ALL)
OlympicsAllProvider = _make_sports_provider("culture:sports:olympics:all", OLYMPICS_ALL)
SummerOlympicsProvider = _make_sports_provider("culture:sports:olympics:summer", SUMMER_OLYMPICS_ALL)
WinterOlympicsProvider = _make_sports_provider("culture:sports:olympics:winter", WINTER_OLYMPICS_ALL)
WorldCupsProvider = _make_sports_provider("culture:sports:fifa world cup", WORLD_CUPS_ALL)
EurosProvider = _make_sports_provider("culture:sports:uefa euro", EUROS_ALL)
FootballClubsProvider = _make_sports_provider("culture:sports:football clubs", FOOTBALL_CLUBS_ALL)


# -- Brands --

def _make_brands_provider(key, item_list):
    class BrandsProvider(CategoryProvider):
        light_bg = True
        override_name = True

        def get_image(self, item):
            if item in LOGOS:
                return {"name": item, "image": LOGOS[item]}
            return None

        def get_tag(self, item):
            return BRAND_TAGS.get(item)

    BrandsProvider.key = key
    BrandsProvider.items = item_list
    return BrandsProvider


BrandsAllProvider = _make_brands_provider("culture:brands:all", BRAND_ALL_NAMES)
BrandsTechProvider = _make_brands_provider("culture:brands:tech", TECH_NAMES)
BrandsAutoProvider = _make_brands_provider("culture:brands:automotive", AUTOMOTIVE_NAMES)
BrandsFashionProvider = _make_brands_provider("culture:brands:fashion", FASHION_NAMES)
BrandsFoodProvider = _make_brands_provider("culture:brands:food & drink", FOOD_AND_DRINK_NAMES)
BrandsAirlinesProvider = _make_brands_provider("culture:brands:airlines", AIRLINES_NAMES)


# -- Register all --

register(MonumentsProvider())
register(PaintingMovementsProvider())
register(PaintersProvider())
register(PaintingsProvider())
register(CharAllProvider())
register(CharStarWarsProvider())
register(CharLotrProvider())
register(CharHPProvider())
register(CharDisneyProvider())
register(CharMarvelProvider())
register(CharDCProvider())
register(CharAnimeProvider())
register(ActorsProvider())
register(DirectorsProvider())
register(MoviePostersProvider())
register(MovieScenesProvider())
register(TVShowsProvider())
register(AlbumsProvider())
register(InstrumentsProvider())
register(SportsAllProvider())
register(OlympicsAllProvider())
register(SummerOlympicsProvider())
register(WinterOlympicsProvider())
register(WorldCupsProvider())
register(EurosProvider())
register(FootballClubsProvider())
register(BrandsAllProvider())
register(BrandsTechProvider())
register(BrandsAutoProvider())
register(BrandsFashionProvider())
register(BrandsFoodProvider())
register(BrandsAirlinesProvider())
