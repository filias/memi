"""Nature providers: animals, plants, landscapes, rocks & minerals, space, nature:all."""

from memi_engine import CategoryProvider, ScientificNameProvider, register
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
from memi.categories.minerals import (
    ALL as MINERALS_ALL,
    TYPES as MINERAL_TYPES,
    TYPE_LABEL as MINERAL_TYPE_LABEL,
)
from memi.categories.scientific_names import SCIENTIFIC_NAMES


_DINOSAUR_SET = set(DINOSAUR_LIST)


class AnimalsProvider(ScientificNameProvider):
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


class PlantsAllProvider(ScientificNameProvider):
    key = "nature:plants:all"
    items = PLANT_ALL


class FlowersProvider(ScientificNameProvider):
    key = "nature:plants:flowers"
    items = FLOWERS


class FruitsAndVegProvider(ScientificNameProvider):
    key = "nature:plants:fruits & vegetables"
    items = FRUITS_AND_VEGETABLES


class HouseplantsProvider(ScientificNameProvider):
    key = "nature:plants:houseplants"
    items = HOUSEPLANTS


class PlantOtherProvider(ScientificNameProvider):
    key = "nature:plants:other"
    items = PLANT_OTHER


class TreesProvider(ScientificNameProvider):
    key = "nature:plants:trees"
    items = TREES


class LandscapesProvider(CategoryProvider):
    key = "nature:landscapes"
    items = LANDSCAPE_LIST
    filters = {
        "continents": LANDSCAPE_CONTINENTS,
    }

    def get_tag(self, item):
        return NATURE_LOCATIONS.get(item)


class RocksMineralsProvider(CategoryProvider):
    key = "nature:rocks & minerals"
    items = MINERALS_ALL
    filters = {
        "type": MINERAL_TYPES,
    }

    def get_tag(self, item):
        return MINERAL_TYPE_LABEL.get(item)


class NatureAllProvider(CategoryProvider):
    key = "nature:all"
    items = ANIMAL_LIST + PLANT_ALL + LANDSCAPE_LIST + MINERALS_ALL + SPACE_ALL

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
        if item in MINERAL_TYPE_LABEL:
            return MINERAL_TYPE_LABEL[item]
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
register(RocksMineralsProvider())
register(NatureAllProvider())
register(SpaceAllProvider())
register(SolarSystemProvider())
register(DeepSpaceProvider())
