"""Nature providers: animals, plants, landscapes, nature:all, space."""

from memi_engine import CategoryProvider, register
from memi_engine import images

from memi.categories.animals import ALL as ANIMAL_LIST
from memi.categories.animals import CLASSES as ANIMAL_CLASSES
from memi.categories.animals import DIFFICULTY as ANIMAL_DIFFICULTY
from memi.categories.dinosaurs import ALL as DINOSAUR_LIST
from memi.categories.plants import (
    ALL as PLANT_ALL,
    FLOWERS,
    FRUITS_AND_VEGETABLES,
    HOUSEPLANTS,
    OTHER as PLANT_OTHER,
    TREES,
)
from memi.categories.nature import (
    ALL as LANDSCAPE_LIST,
    CONTINENTS as LANDSCAPE_CONTINENTS,
    LOCATIONS as NATURE_LOCATIONS,
)
from memi.categories.space import (
    ALL as SPACE_ALL,
    SOLAR_SYSTEM,
    DEEP_SPACE,
    LOCATIONS as SPACE_LOCATIONS,
)
from memi.categories.scientific_names import SCIENTIFIC_NAMES


_DINOSAUR_SET = set(DINOSAUR_LIST)


class AnimalsProvider(CategoryProvider):
    key = "nature:animals"
    items = ANIMAL_LIST
    filters = {
        "classes": ANIMAL_CLASSES,
        "difficulty": ANIMAL_DIFFICULTY,
    }

    def get_image(self, item):
        if item in _DINOSAUR_SET:
            result = images.get_dino_image(item)
            if result and result.get("image"):
                return result
        return images.get_wikipedia_image(item)

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        return None


class PlantsAllProvider(CategoryProvider):
    key = "nature:plants:all"
    items = PLANT_ALL

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        return None


class FlowersProvider(CategoryProvider):
    key = "nature:plants:flowers"
    items = FLOWERS

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        return None


class FruitsAndVegProvider(CategoryProvider):
    key = "nature:plants:fruits & vegetables"
    items = FRUITS_AND_VEGETABLES

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        return None


class HouseplantsProvider(CategoryProvider):
    key = "nature:plants:houseplants"
    items = HOUSEPLANTS

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        return None


class PlantOtherProvider(CategoryProvider):
    key = "nature:plants:other"
    items = PLANT_OTHER

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        return None


class TreesProvider(CategoryProvider):
    key = "nature:plants:trees"
    items = TREES

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        return None


class LandscapesProvider(CategoryProvider):
    key = "nature:landscapes"
    items = LANDSCAPE_LIST
    filters = {
        "continents": LANDSCAPE_CONTINENTS,
    }

    def get_tag(self, item):
        return NATURE_LOCATIONS.get(item)


class NatureAllProvider(CategoryProvider):
    key = "nature:all"
    items = ANIMAL_LIST + PLANT_ALL + LANDSCAPE_LIST + SPACE_ALL

    def get_image(self, item):
        if item in _DINOSAUR_SET:
            result = images.get_dino_image(item)
            if result and result.get("image"):
                return result
        return images.get_wikipedia_image(item)

    def get_tag(self, item):
        sci = SCIENTIFIC_NAMES.get(item, "")
        if sci and sci.lower() != item.lower():
            return sci
        if item in NATURE_LOCATIONS:
            return NATURE_LOCATIONS[item]
        if item in SPACE_LOCATIONS:
            return SPACE_LOCATIONS[item]
        return None


class SpaceAllProvider(CategoryProvider):
    key = "nature:space:all"
    items = SPACE_ALL

    def get_tag(self, item):
        return SPACE_LOCATIONS.get(item)


class SolarSystemProvider(CategoryProvider):
    key = "nature:space:solar system"
    items = SOLAR_SYSTEM

    def get_tag(self, item):
        return SPACE_LOCATIONS.get(item)


class DeepSpaceProvider(CategoryProvider):
    key = "nature:space:deep space"
    items = DEEP_SPACE

    def get_tag(self, item):
        return SPACE_LOCATIONS.get(item)


register(AnimalsProvider())
register(PlantsAllProvider())
register(FlowersProvider())
register(FruitsAndVegProvider())
register(HouseplantsProvider())
register(PlantOtherProvider())
register(TreesProvider())
register(LandscapesProvider())
register(NatureAllProvider())
register(SpaceAllProvider())
register(SolarSystemProvider())
register(DeepSpaceProvider())
