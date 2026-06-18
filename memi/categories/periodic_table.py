"""Chemical elements (periodic table) for the Science category.

The card shows a periodic-table tile (atomic number + symbol); the answer
is the element name. Element data is generated into _periodic_data.py by
scripts/gen_periodic_table.py; the tiles are drawn by
scripts/render_periodic_table.py. `category` (the element series) is the filter.
"""

import re

from memi.categories._periodic_data import ELEMENTS

ALL = list(ELEMENTS)

# category (series) -> [names], for the filter UI
CATEGORIES: dict[str, list[str]] = {}
for _name, _data in ELEMENTS.items():
    CATEGORIES.setdefault(_data["category"].lower(), []).append(_name)


def slug(name: str) -> str:
    """Filename-safe slug for an element name (matches the rendered tile)."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
