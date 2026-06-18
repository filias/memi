"""Science providers: formulas (guess what each formula is for)."""

from memi_engine import CategoryProvider, register

from memi.categories.formulas import ALL as FORMULA_LIST
from memi.categories.formulas import FIELDS as FORMULA_FIELDS
from memi.categories.formulas import FORMULAS, slug


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


register(FormulasProvider())
