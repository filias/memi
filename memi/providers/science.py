"""Science providers: formulas, sequences, periodic table and materials."""

from memi_engine import CategoryProvider, register

from memi.categories.formulas import ALL as FORMULA_LIST
from memi.categories.formulas import FIELDS as FORMULA_FIELDS
from memi.categories.formulas import FORMULAS, slug
from memi.categories.materials import ALL as MATERIAL_LIST
from memi.categories.materials import TYPES as MATERIAL_TYPES
from memi.categories.materials import tag_for as material_tag
from memi.categories.periodic_table import ALL as ELEMENT_LIST
from memi.categories.periodic_table import CATEGORIES as ELEMENT_CATEGORIES
from memi.categories.periodic_table import ELEMENTS
from memi.categories.periodic_table import slug as el_slug
from memi.categories.sequences import ALL as SEQUENCE_LIST
from memi.categories.sequences import KINDS as SEQUENCE_KINDS
from memi.categories.sequences import SEQUENCES
from memi.categories.sequences import slug as seq_slug


class FormulasProvider(CategoryProvider):
    key = "science:formulas"
    items = FORMULA_LIST
    light_bg = True  # dark formula glyphs on a white card
    override_name = True
    filters = {
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
    filters = {
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
    filters = {
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
    filters = {
        "type": MATERIAL_TYPES,
    }

    def get_tag(self, item):
        return material_tag(item)


register(FormulasProvider())
register(SequencesProvider())
register(PeriodicTableProvider())
register(MaterialsProvider())
