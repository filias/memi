"""Road signs from around the world. Images sourced from Wikimedia Commons SVGs."""

# Each sign: (display_name, commons_file, region_tag)
# region_tag shown after reveal; empty string for international signs
SIGNS = [
    # International / Vienna Convention
    ("Stop", "Vienna Convention road sign B2a.svg", ""),
    ("Yield / Give way", "Vienna Convention road sign B1-V1.svg", ""),
    ("No entry", "Vienna Convention road sign C3a-V3-1.svg", ""),
    ("Speed limit 30", "Vienna Convention road sign C14-V1-30.svg", ""),
    ("Speed limit 50", "Vienna Convention road sign C14-V1-50.svg", ""),
    ("Speed limit 60", "Vienna Convention road sign C14-V1-60.svg", ""),
    ("Pedestrian crossing", "Vienna Convention road sign Aa-21a-V1.svg", ""),
    ("Roundabout", "Vienna Convention road sign D3a.svg", ""),
    ("No parking", "Vienna Convention road sign C18-V1.svg", ""),
    ("No overtaking", "Vienna Convention road sign C13aa-V1.svg", ""),
    ("Priority road", "Vienna Convention road sign B3-V1.svg", ""),
    ("One way", "Vienna Convention road sign E3b-V2.svg", ""),
    ("Road works", "Vienna Convention road sign Aa-16-V1.svg", ""),
    ("Level crossing", "Vienna Convention road sign A-28a-V1-1.svg", ""),
    ("Falling rocks", "Vienna Convention road sign Aa-11a-V1.svg", ""),
    ("Dead end", "Vienna Convention road sign G13.svg", ""),
    ("Pedestrian crossing info", "Vienna Convention road sign E12aa-V4.svg", ""),
    # Country-specific
    ("Kangaroo warning", "Australia road sign W5-29.svg", "Australia"),
    ("Moose warning", "Sweden road sign A19-1.svg", "Sweden"),
    ("Deer crossing", "MUTCD W11-3.svg", "USA"),
    ("Elephant crossing", "Thailand road sign ต-ระวังช้างป่า.svg", "Thailand"),
    ("Camel crossing", "SA road sign - Camels crossing.svg", "Saudi Arabia"),
    ("Stop / 止まれ", "Japan road sign 330-B.svg", "Japan"),
    ("No entry", "Japan road sign 303.svg", "Japan"),
    ("Interstate highway", "I-blank (1957).svg", "USA"),
    ("Railroad crossbuck", "American Crossbuck (MUTCD R15-1).svg", "USA"),
    ("National speed limit", "UK traffic sign 671.svg", "UK"),
]

ALL = [s[0] for s in SIGNS]
COMMONS_FILES = {s[0]: s[1] for s in SIGNS}
REGIONS = {s[0]: s[2] for s in SIGNS}
