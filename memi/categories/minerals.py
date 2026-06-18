"""Rocks, minerals & gemstones for the Nature category.

Three groups exposed as a "type" filter: minerals (natural inorganic
species), rocks (aggregates), and gemstones (cut/precious varieties).
Some gemstones are varieties of a mineral also listed here (e.g. Ruby is a
variety of Corundum) — that overlap is intentional and fine for guessing.
"""

MINERALS = [
    "Quartz",
    "Pyrite",
    "Galena",
    "Hematite",
    "Magnetite",
    "Malachite",
    "Azurite",
    "Fluorite",
    "Calcite",
    "Gypsum",
    "Halite",
    "Sulfur",
    "Graphite",
    "Cinnabar",
    "Baryte",
    "Olivine",
    "Beryl",
    "Corundum",
    "Rhodochrosite",
    "Stibnite",
    "Bornite",
    "Chalcopyrite",
    "Labradorite",
    "Vanadinite",
    "Wulfenite",
    "Aragonite",
    "Apatite",
    "Feldspar",
    "Mica",
    "Talc",
    "Sodalite",
    "Rhodonite",
    "Selenite (gypsum)",
    "Celestine (mineral)",
]

ROCKS = [
    "Granite",
    "Basalt",
    "Obsidian",
    "Marble",
    "Limestone",
    "Sandstone",
    "Slate",
    "Shale",
    "Gneiss",
    "Schist",
    "Pumice",
    "Quartzite",
    "Breccia",
    "Tuff",
    "Gabbro",
    "Diorite",
    "Andesite",
    "Rhyolite",
    "Travertine",
    "Chalk",
    "Flint",
    "Coal",
    "Anthracite",
    "Chert",
    "Conglomerate (geology)",
]

GEMSTONES = [
    "Diamond",
    "Ruby",
    "Sapphire",
    "Emerald",
    "Amethyst",
    "Topaz",
    "Opal",
    "Garnet",
    "Aquamarine (gem)",
    "Peridot",
    "Tanzanite",
    "Tourmaline",
    "Turquoise",
    "Jade",
    "Lapis lazuli",
    "Citrine",
    "Moonstone (gemstone)",
    "Agate",
    "Onyx",
    "Spinel",
    "Zircon",
    "Chrysoberyl",
    "Tiger's eye",
    "Amber",
    "Pearl",
]

ALL = MINERALS + ROCKS + GEMSTONES

TYPES = {
    "minerals": MINERALS,
    "rocks": ROCKS,
    "gemstones": GEMSTONES,
}

# item -> tag shown on the revealed card
TYPE_LABEL = {
    **{name: "Mineral" for name in MINERALS},
    **{name: "Rock" for name in ROCKS},
    **{name: "Gemstone" for name in GEMSTONES},
}
