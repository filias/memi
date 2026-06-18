"""Metals for the Science category.

The card shows a photo of the metal; the answer is its name. Pure metals
carry their chemical symbol as the reveal tag, alloys their composition.
`kind` (elements / alloys) is the filter. Images come from Wikipedia.
"""

METALS = {
    # Pure metals — tag is the element symbol
    "Gold": {"kind": "element", "tag": "Au"},
    "Silver": {"kind": "element", "tag": "Ag"},
    "Copper": {"kind": "element", "tag": "Cu"},
    "Iron": {"kind": "element", "tag": "Fe"},
    "Aluminium": {"kind": "element", "tag": "Al"},
    "Titanium": {"kind": "element", "tag": "Ti"},
    "Zinc": {"kind": "element", "tag": "Zn"},
    "Tin": {"kind": "element", "tag": "Sn"},
    "Lead": {"kind": "element", "tag": "Pb"},
    "Nickel": {"kind": "element", "tag": "Ni"},
    "Platinum": {"kind": "element", "tag": "Pt"},
    "Mercury (element)": {"kind": "element", "tag": "Hg"},
    "Tungsten": {"kind": "element", "tag": "W"},
    "Chromium": {"kind": "element", "tag": "Cr"},
    "Cobalt": {"kind": "element", "tag": "Co"},
    "Magnesium": {"kind": "element", "tag": "Mg"},
    "Bismuth": {"kind": "element", "tag": "Bi"},
    "Manganese": {"kind": "element", "tag": "Mn"},
    "Palladium": {"kind": "element", "tag": "Pd"},
    "Uranium": {"kind": "element", "tag": "U"},
    "Lithium": {"kind": "element", "tag": "Li"},
    "Sodium": {"kind": "element", "tag": "Na"},
    "Gallium": {"kind": "element", "tag": "Ga"},
    # Alloys — tag is the composition
    "Bronze": {"kind": "alloy", "tag": "Copper + tin"},
    "Brass": {"kind": "alloy", "tag": "Copper + zinc"},
    "Steel": {"kind": "alloy", "tag": "Iron + carbon"},
    "Stainless steel": {"kind": "alloy", "tag": "Iron + chromium"},
    "Cast iron": {"kind": "alloy", "tag": "Iron + carbon"},
    "Cupronickel": {"kind": "alloy", "tag": "Copper + nickel"},
    "Sterling silver": {"kind": "alloy", "tag": "Silver + copper"},
    "Duralumin": {"kind": "alloy", "tag": "Aluminium + copper"},
    "Solder": {"kind": "alloy", "tag": "Tin + lead"},
    "White gold": {"kind": "alloy", "tag": "Gold + palladium"},
    "Electrum": {"kind": "alloy", "tag": "Gold + silver"},
    "Amalgam (dentistry)": {"kind": "alloy", "tag": "Mercury alloy"},
}

ALL = list(METALS)

# kind -> [names], for the filter UI
KINDS: dict[str, list[str]] = {"elements": [], "alloys": []}
for _name, _data in METALS.items():
    KINDS["elements" if _data["kind"] == "element" else "alloys"].append(_name)
