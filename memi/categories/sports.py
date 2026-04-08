"""Sports events: Olympic Games, FIFA World Cup, UEFA Euro."""

# (display_name, wikipedia_article, image_file_or_none, tag)
# image_file is the exact Wikipedia File: name, or None to use article image

OLYMPICS = [
    ("Athens 1896", "1896 Summer Olympics", None, "Greece"),
    ("Paris 1900", "1900 Summer Olympics", None, "France"),
    ("St. Louis 1904", "1904 Summer Olympics", None, "USA"),
    ("London 1908", "1908 Summer Olympics", None, "UK"),
    ("Stockholm 1912", "1912 Summer Olympics", None, "Sweden"),
    ("Antwerp 1920", "1920 Summer Olympics", None, "Belgium"),
    ("Paris 1924", "1924 Summer Olympics", "1924 Summer Olympics logo.svg", "France"),
    ("Amsterdam 1928", "1928 Summer Olympics", None, "Netherlands"),
    (
        "Los Angeles 1932",
        "1932 Summer Olympics",
        "1932 Summer Olympics logo.svg",
        "USA",
    ),
    ("Berlin 1936", "1936 Summer Olympics", "1936 Summer Olympics logo.svg", "Germany"),
    ("London 1948", "1948 Summer Olympics", None, "UK"),
    (
        "Helsinki 1952",
        "1952 Summer Olympics",
        "1952 Summer Olympics logo.svg",
        "Finland",
    ),
    (
        "Melbourne 1956",
        "1956 Summer Olympics",
        "1956 Summer Olympics logo.svg",
        "Australia",
    ),
    ("Rome 1960", "1960 Summer Olympics", "1960 Summer Olympics logo.png", "Italy"),
    ("Tokyo 1964", "1964 Summer Olympics", None, "Japan"),
    ("Mexico City 1968", "1968 Summer Olympics", None, "Mexico"),
    ("Munich 1972", "1972 Summer Olympics", "1972 Summer Olympics logo.svg", "Germany"),
    (
        "Montreal 1976",
        "1976 Summer Olympics",
        "1976 Summer Olympics logo.svg",
        "Canada",
    ),
    ("Moscow 1980", "1980 Summer Olympics", None, "Soviet Union"),
    (
        "Los Angeles 1984",
        "1984 Summer Olympics",
        "1984 Summer Olympics logo.svg",
        "USA",
    ),
    (
        "Seoul 1988",
        "1988 Summer Olympics",
        "1988 Summer Olympics logo.svg",
        "South Korea",
    ),
    (
        "Barcelona 1992",
        "1992 Summer Olympics",
        "1992 Summer Olympics logo.svg",
        "Spain",
    ),
    ("Atlanta 1996", "1996 Summer Olympics", "1996 Summer Olympics logo.svg", "USA"),
    (
        "Sydney 2000",
        "2000 Summer Olympics",
        "2000 Summer Olympics logo.svg",
        "Australia",
    ),
    ("Athens 2004", "2004 Summer Olympics", "2004 Summer Olympics logo.svg", "Greece"),
    ("Beijing 2008", "2008 Summer Olympics", "2008 Summer Olympics logo.svg", "China"),
    ("London 2012", "2012 Summer Olympics", "2012 Summer Olympics logo.svg", "UK"),
    ("Rio 2016", "2016 Summer Olympics", "2016 Summer Olympics logo.svg", "Brazil"),
    ("Tokyo 2020", "2020 Summer Olympics", "2020 Summer Olympics logo.svg", "Japan"),
    ("Paris 2024", "2024 Summer Olympics", "2024 Summer Olympics logo.svg", "France"),
]

WORLD_CUPS = [
    ("Uruguay 1930", "1930 FIFA World Cup", None, "Winner: Uruguay"),
    (
        "Italy 1934",
        "1934 FIFA World Cup",
        "1934 fifa worldcup poster.jpg",
        "Winner: Italy",
    ),
    (
        "France 1938",
        "1938 FIFA World Cup",
        "1938 fifa worldcup poster.jpg",
        "Winner: Italy",
    ),
    ("Brazil 1950", "1950 FIFA World Cup", None, "Winner: Uruguay"),
    ("Switzerland 1954", "1954 FIFA World Cup", None, "Winner: West Germany"),
    (
        "Sweden 1958",
        "1958 FIFA World Cup",
        "1958 Football World Cup poster.jpg",
        "Winner: Brazil",
    ),
    (
        "Chile 1962",
        "1962 FIFA World Cup",
        "1962 Football World Cup poster.jpg",
        "Winner: Brazil",
    ),
    (
        "England 1966",
        "1966 FIFA World Cup",
        "1966 FIFA World Cup logo.png",
        "Winner: England",
    ),
    ("Mexico 1970", "1970 FIFA World Cup", None, "Winner: Brazil"),
    (
        "West Germany 1974",
        "1974 FIFA World Cup",
        "FIFA World Cup 1974 - emblem.svg",
        "Winner: West Germany",
    ),
    ("Argentina 1978", "1978 FIFA World Cup", None, "Winner: Argentina"),
    ("Spain 1982", "1982 FIFA World Cup", None, "Winner: Italy"),
    ("Mexico 1986", "1986 FIFA World Cup", None, "Winner: Argentina"),
    ("Italy 1990", "1990 FIFA World Cup", None, "Winner: West Germany"),
    ("USA 1994", "1994 FIFA World Cup", None, "Winner: Brazil"),
    (
        "France 1998",
        "1998 FIFA World Cup",
        "1998 FIFA World Cup logo.svg",
        "Winner: France",
    ),
    (
        "South Korea/Japan 2002",
        "2002 FIFA World Cup",
        "2002 FIFA World Cup logo.svg",
        "Winner: Brazil",
    ),
    ("Germany 2006", "2006 FIFA World Cup", None, "Winner: Italy"),
    (
        "South Africa 2010",
        "2010 FIFA World Cup",
        "2010 FIFA World Cup logo.svg",
        "Winner: Spain",
    ),
    ("Brazil 2014", "2014 FIFA World Cup", None, "Winner: Germany"),
    ("Russia 2018", "2018 FIFA World Cup", None, "Winner: France"),
    ("Qatar 2022", "2022 FIFA World Cup", None, "Winner: Argentina"),
]

EUROS = [
    (
        "France 1960",
        "UEFA Euro 1960",
        "UEFA Euro 1960 logo.svg",
        "Winner: Soviet Union",
    ),
    ("Spain 1964", "UEFA Euro 1964", "UEFA Euro 1964 logo.svg", "Winner: Spain"),
    ("Italy 1968", "UEFA Euro 1968", "UEFA Euro 1968 logo.svg", "Winner: Italy"),
    (
        "Belgium 1972",
        "UEFA Euro 1972",
        "UEFA Euro 1972 logo.svg",
        "Winner: West Germany",
    ),
    (
        "Yugoslavia 1976",
        "UEFA Euro 1976",
        "UEFA Euro 1976 logo.svg",
        "Winner: Czechoslovakia",
    ),
    ("Italy 1980", "UEFA Euro 1980", "UEFA Euro 1980 logo.svg", "Winner: West Germany"),
    ("France 1984", "UEFA Euro 1984", "UEFA Euro 1984 logo.svg", "Winner: France"),
    (
        "West Germany 1988",
        "UEFA Euro 1988",
        "UEFA Euro 1988 logo.svg",
        "Winner: Netherlands",
    ),
    ("Sweden 1992", "UEFA Euro 1992", "UEFA Euro 1992 logo.svg", "Winner: Denmark"),
    ("England 1996", "UEFA Euro 1996", "UEFA Euro 1996 logo.svg", "Winner: Germany"),
    (
        "Belgium/Netherlands 2000",
        "UEFA Euro 2000",
        "UEFA Euro 2000 logo.svg",
        "Winner: France",
    ),
    ("Portugal 2004", "UEFA Euro 2004", "UEFA Euro 2004 logo.svg", "Winner: Greece"),
    ("Austria/Switzerland 2008", "UEFA Euro 2008", None, "Winner: Spain"),
    (
        "Poland/Ukraine 2012",
        "UEFA Euro 2012",
        "UEFA Euro 2012 logo.svg",
        "Winner: Spain",
    ),
    ("France 2016", "UEFA Euro 2016", "UEFA Euro 2016 logo.svg", "Winner: Portugal"),
    ("Europe 2020", "UEFA Euro 2020", "UEFA Euro 2020 logo.svg", "Winner: Italy"),
    ("Germany 2024", "UEFA Euro 2024", "UEFA Euro 2024 logo.svg", "Winner: Spain"),
]

OLYMPICS_ALL = [e[0] for e in OLYMPICS]
WORLD_CUPS_ALL = [e[0] for e in WORLD_CUPS]
EUROS_ALL = [e[0] for e in EUROS]

# Lookup dicts
_ALL_EVENTS = OLYMPICS + WORLD_CUPS + EUROS
WIKIPEDIA = {e[0]: e[1] for e in _ALL_EVENTS}
IMAGE_FILES = {e[0]: e[2] for e in _ALL_EVENTS}
TAGS = {e[0]: e[3] for e in _ALL_EVENTS}
