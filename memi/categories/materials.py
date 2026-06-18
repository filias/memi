"""Materials for the Science category.

The card shows a photo of the material; the answer is its name. `type` is
the filter and is shown as the reveal tag. Images come from Wikipedia.
Stone/minerals (marble, granite, …) intentionally live in nature:rocks &
minerals, so they're not duplicated here.
"""

# name -> type
MATERIALS = {
    # Metals (pure)
    "Copper": "metals",
    "Gold": "metals",
    "Aluminium": "metals",
    "Titanium": "metals",
    # Alloys
    "Bronze": "alloys",
    "Brass": "alloys",
    "Steel": "alloys",
    "Stainless steel": "alloys",
    "Cast iron": "alloys",
    # Polymers / plastics
    "Natural rubber": "polymers",
    "Silicone": "polymers",
    "Nylon": "polymers",
    "Polystyrene": "polymers",
    "Polyethylene": "polymers",
    "Polyvinyl chloride": "polymers",
    # Ceramics & glass
    "Glass": "ceramics & glass",
    "Porcelain": "ceramics & glass",
    "Brick": "ceramics & glass",
    "Earthenware": "ceramics & glass",
    # Wood
    "Wood": "wood",
    "Bamboo": "wood",
    "Cork (material)": "wood",
    "Plywood": "wood",
    # Textiles
    "Cotton": "textiles",
    "Wool": "textiles",
    "Silk": "textiles",
    "Leather": "textiles",
    "Denim": "textiles",
    "Linen": "textiles",
    # Composites
    "Carbon fibers": "composites",
    "Glass fiber": "composites",
    "Concrete": "composites",
    "Reinforced concrete": "composites",
    # Paper
    "Paper": "paper",
    "Cardboard": "paper",
}

ALL = list(MATERIALS)

# type -> [names], for the filter UI
TYPES: dict[str, list[str]] = {}
for _name, _type in MATERIALS.items():
    TYPES.setdefault(_type, []).append(_name)

TYPE_LABEL = {
    "metals": "Metal",
    "alloys": "Alloy",
    "polymers": "Polymer",
    "ceramics & glass": "Ceramic / glass",
    "wood": "Wood",
    "textiles": "Textile",
    "composites": "Composite",
    "paper": "Paper",
}


def tag_for(name: str) -> str:
    """Reveal tag: the material's type."""
    return TYPE_LABEL[MATERIALS[name]]
