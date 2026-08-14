"""Science providers: formulas, sequences, periodic table and materials."""

from typing import ClassVar

from memi_engine import CategoryProvider, register

from memi.categories.formulas import (
    ALL as FORMULA_LIST,
    FIELDS as FORMULA_FIELDS,
    FORMULAS,
    slug,
)
from memi.categories.materials import (
    ALL as MATERIAL_LIST,
    TYPES as MATERIAL_TYPES,
    tag_for as material_tag,
)
from memi.categories.periodic_table import (
    ALL as ELEMENT_LIST,
    CATEGORIES as ELEMENT_CATEGORIES,
    ELEMENTS,
    slug as el_slug,
)
from memi.categories.sequences import (
    ALL as SEQUENCE_LIST,
    KINDS as SEQUENCE_KINDS,
    SEQUENCES,
    slug as seq_slug,
)


class FormulasProvider(CategoryProvider):
    key = "science:formulas"
    items = FORMULA_LIST
    light_bg = True  # dark formula glyphs on a white card
    override_name = True
    filters: ClassVar[dict[str, dict[str, list[str]]]] = {
        "field": FORMULA_FIELDS,
    }

    def get_image(self, item):
        # Pre-rendered by scripts/render_formulas.py
        return {"name": item, "image": f"/static/img/formulas/{slug(item)}.svg"}

    def get_clue(self, item):
        # Show the field (e.g. "Geometry") as a gentle pre-reveal hint.
        return FORMULAS[item]["field"].capitalize()


class SequencesProvider(CategoryProvider):
    key = "science:sequences"
    items = SEQUENCE_LIST
    light_bg = True  # dark numerals on a white card
    filters: ClassVar[dict[str, dict[str, list[str]]]] = {
        "kind": SEQUENCE_KINDS,
    }

    def get_image(self, item):
        # The answer is the next term; the prompt SVG shows "…, ?".
        return {"name": str(SEQUENCES[item]["next"]), "image": f"/static/img/sequences/{seq_slug(item)}.svg"}

    def get_tag(self, item):
        # Reveal which sequence it was.
        return item


class PeriodicTableProvider(CategoryProvider):
    key = "science:periodic table"
    items = ELEMENT_LIST
    light_bg = True  # dark tile on a white card
    filters: ClassVar[dict[str, dict[str, list[str]]]] = {
        "category": ELEMENT_CATEGORIES,
    }

    def get_image(self, item):
        # Tile (atomic number + symbol) pre-rendered by render_periodic_table.py
        return {"name": item, "image": f"/static/img/elements/{el_slug(item)}.svg"}

    def get_tag(self, item):
        return ELEMENTS[item]["category"]


class MaterialsProvider(CategoryProvider):
    key = "science:materials"
    items = MATERIAL_LIST
    filters: ClassVar[dict[str, dict[str, list[str]]]] = {
        "type": MATERIAL_TYPES,
    }

    def get_tag(self, item):
        return material_tag(item)


register(FormulasProvider())
register(SequencesProvider())
register(PeriodicTableProvider())
register(MaterialsProvider())
