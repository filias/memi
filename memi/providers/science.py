"""Science providers: formulas, sequences (guess the next term) and metals."""

from memi_engine import CategoryProvider, register

from memi.categories.formulas import ALL as FORMULA_LIST
from memi.categories.formulas import FIELDS as FORMULA_FIELDS
from memi.categories.formulas import FORMULAS, slug
from memi.categories.metals import ALL as METAL_LIST
from memi.categories.metals import KINDS as METAL_KINDS
from memi.categories.metals import METALS
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


class MetalsProvider(CategoryProvider):
    key = "science:metals"
    items = METAL_LIST
    filters = {
        "kind": METAL_KINDS,
    }

    def get_tag(self, item):
        # Symbol for pure metals, composition for alloys.
        return METALS[item]["tag"]


register(FormulasProvider())
register(SequencesProvider())
register(MetalsProvider())
