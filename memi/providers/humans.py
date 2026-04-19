"""Humans providers: bones, people."""

from memi_engine import CategoryProvider, register
from memi_engine import images

from memi.categories.bones import ALL as BONE_LIST
from memi.categories.people import ALL as PEOPLE_LIST, ROLES as PEOPLE_ROLES


class BonesProvider(CategoryProvider):
    key = "humans:bones"
    items = BONE_LIST
    footers = ["eskeletons"]

    def get_image(self, item):
        return images.get_bone_image(item)


class PeopleProvider(CategoryProvider):
    key = "humans:people"
    items = PEOPLE_LIST
    filters = {
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
