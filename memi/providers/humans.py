"""Humans providers: bones, people."""

from typing import ClassVar

from memi_engine import CategoryProvider, images, register

from memi.categories.bones import ALL as BONE_LIST
from memi.categories.people import ALL as PEOPLE_LIST, ROLES as PEOPLE_ROLES


class BonesProvider(CategoryProvider):
    key = "humans:bones"
    items = BONE_LIST
    footers: ClassVar[list[str]] = ["eskeletons"]

    def get_image(self, item):
        return images.get_bone_image(item)


class PeopleProvider(CategoryProvider):
    key = "humans:people"
    items = PEOPLE_LIST
    filters: ClassVar[dict[str, dict[str, list[str]]]] = {
        "roles": PEOPLE_ROLES,
    }

    def get_tag(self, item):
        desc = images.get_wikipedia_description(item)
        if desc:
            desc = desc.replace("(born ", "(").replace("(", "").replace(")", "")
            return desc
        return None


register(BonesProvider())
register(PeopleProvider())
