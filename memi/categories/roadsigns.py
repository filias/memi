"""Road signs from around the world."""

# Each sign: (display_name, wikipedia_article, region_tag)
# region_tag is shown after reveal; empty string for international signs

SIGNS = [
    # International / Vienna Convention
    ("Stop sign", "Stop sign", ""),
    ("Yield / Give way", "Yield sign", ""),
    ("No entry", "No entry sign", ""),
    ("Pedestrian crossing", "Pedestrian crossing", ""),
    ("Speed limit", "Speed limit", ""),
    ("Level crossing", "Level crossing", ""),
    ("One-way traffic", "One-way traffic", ""),
    ("Road works", "Road works", ""),
    ("Roundabout", "Roundabout", ""),
    ("No parking", "Parking", ""),
    # Signs with own articles
    ("Crossbuck (railroad)", "Crossbuck", "USA"),
    ("School zone", "School zone", ""),
    ("Zebra crossing", "Zebra crossing", "UK"),
    ("Pelican crossing", "Pelican crossing", "UK"),
    ("National speed limit", "National speed limit", "UK"),
    ("Autobahn", "Autobahn", "Germany"),
    ("Wildlife crossing", "Wildlife crossing", ""),
    # Animal warnings (distinctive & fun)
    ("Moose warning", "Road signs in Sweden", "Scandinavia"),
    ("Kangaroo warning", "Road signs in Australia", "Australia"),
    ("Koala warning", "Road signs in Australia", "Australia"),
    ("Wombat warning", "Road signs in Australia", "Australia"),
    ("Elephant warning", "Road signs in Thailand", "Thailand"),
    ("Camel warning", "Road signs in Israel", "Israel"),
    ("Deer crossing", "Road signs in the United States", "USA"),
    ("Penguin warning", "Road signs in New Zealand", "New Zealand"),
    # European
    ("Priority road", "Priority signs", "Europe"),
    ("End of speed limit", "Comparison of European road signs", "Europe"),
    ("No overtaking", "Comparison of European road signs", "Europe"),
    ("Built-up area entry", "Comparison of European road signs", "Europe"),
    # Japan (uniquely shaped)
    ("Stop / 止まれ", "Road signs in Japan", "Japan"),
    # USA specific
    ("Interstate highway shield", "Interstate Highway System", "USA"),
    ("US Route shield", "United States Numbered Highway System", "USA"),
    ("Do not enter", "Road signs in the United States", "USA"),
    ("Wrong way", "Road signs in the United States", "USA"),
    ("No turn on red", "Road signs in the United States", "USA"),
    ("Four-way stop", "Road signs in the United States", "USA"),
    ("Railroad advance warning", "Railroad crossing", "USA"),
    ("Construction zone", "Road signs in the United States", "USA"),
    # Various countries
    ("Pare / Stop", "Road signs in Brazil", "Brazil"),
    ("Bilingual stop/arrêt", "Road signs in Canada", "Canada"),
    ("Road train warning", "Road signs in Australia", "Australia"),
    ("Give way", "Road signs in Australia", "Australia"),
    ("Tope / Speed bump", "Road signs in Mexico", "Mexico"),
    ("Kiwi crossing", "Road signs in New Zealand", "New Zealand"),
]

ALL = [s[0] for s in SIGNS]

# Lookup dicts
WIKIPEDIA = {s[0]: s[1] for s in SIGNS}
REGIONS = {s[0]: s[2] for s in SIGNS}
