"""Sports: events, disciplines, football clubs, NBA teams."""

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
    (
        "South Africa 2010",
        "2010 FIFA World Cup",
        "2010 FIFA World Cup logo.svg",
        "Winner: Spain",
    ),
    ("Brazil 2014", "2014 FIFA World Cup", None, "Winner: Germany"),
    ("Russia 2018", "2018 FIFA World Cup", None, "Winner: France"),
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

SPORTS = [
    # Team sports
    ("Football", "Association football", None, ""),
    ("Basketball", "Basketball", None, ""),
    ("Baseball", "Baseball", None, ""),
    ("Cricket", "Cricket", None, ""),
    ("Rugby", "Rugby union", None, ""),
    ("Volleyball", "Volleyball", None, ""),
    ("Handball", "Handball", None, ""),
    ("Ice hockey", "Ice hockey", None, ""),
    ("Field hockey", "Field hockey", None, ""),
    ("Water polo", "Water polo", None, ""),
    ("Lacrosse", "Lacrosse", None, ""),
    ("Polo", "Polo", None, ""),
    ("Futsal", "Futsal", None, ""),
    # Racquet sports
    ("Tennis", "Tennis", None, ""),
    ("Badminton", "Badminton", None, ""),
    ("Table tennis", "Table tennis", None, ""),
    ("Squash", "Squash (sport)", None, ""),
    ("Padel", "Padel", None, ""),
    # Athletics & track
    ("100 metres", "100 metres", None, "Athletics"),
    ("Marathon", "Marathon", None, "Athletics"),
    ("High jump", "High jump", None, "Athletics"),
    ("Long jump", "Long jump", None, "Athletics"),
    ("Pole vault", "Pole vault", None, "Athletics"),
    ("Shot put", "Shot put", None, "Athletics"),
    ("Javelin throw", "Javelin throw", None, "Athletics"),
    ("Discus throw", "Discus throw", None, "Athletics"),
    ("Hurdles", "Hurdling", None, "Athletics"),
    ("Decathlon", "Decathlon", None, "Athletics"),
    ("Relay race", "Relay race", None, "Athletics"),
    # Combat sports
    ("Boxing", "Boxing", None, ""),
    ("Judo", "Judo", None, ""),
    ("Karate", "Karate", None, ""),
    ("Taekwondo", "Taekwondo", None, ""),
    ("Wrestling", "Wrestling", None, ""),
    ("Fencing", "Fencing", None, ""),
    ("Sumo", "Sumo", None, ""),
    ("MMA", "Mixed martial arts", None, ""),
    # Water sports
    ("Swimming", "Swimming (sport)", None, ""),
    ("Diving", "Diving (sport)", None, ""),
    ("Surfing", "Surfing", None, ""),
    ("Sailing", "Sailing (sport)", None, ""),
    ("Rowing", "Rowing (sport)", None, ""),
    ("Canoeing", "Canoeing", None, ""),
    ("Synchronized swimming", "Artistic swimming", None, ""),
    # Gymnastics
    ("Artistic gymnastics", "Artistic gymnastics", None, ""),
    ("Rhythmic gymnastics", "Rhythmic gymnastics", None, ""),
    ("Trampoline", "Trampolining", None, ""),
    # Cycling & wheels
    ("Road cycling", "Road cycling", None, ""),
    ("BMX", "BMX", None, ""),
    ("Skateboarding", "Skateboarding", None, ""),
    # Winter sports
    ("Alpine skiing", "Alpine skiing", None, ""),
    ("Cross-country skiing", "Cross-country skiing", None, ""),
    ("Figure skating", "Figure skating", None, ""),
    ("Snowboarding", "Snowboarding", None, ""),
    ("Bobsled", "Bobsleigh", None, ""),
    ("Curling", "Curling", None, ""),
    ("Biathlon", "Biathlon", None, ""),
    # Other
    ("Golf", "Golf", None, ""),
    ("Archery", "Archery", None, ""),
    ("Shooting sports", "Shooting sports", None, ""),
    ("Weightlifting", "Olympic weightlifting", None, ""),
    ("Triathlon", "Triathlon", None, ""),
    ("Rock climbing", "Rock climbing", None, ""),
    ("Equestrian", "Equestrianism", None, ""),
    ("Motorsport", "Motorsport", None, ""),
]

FOOTBALL_CLUBS = [
    # England — Premier League
    ("Arsenal", "Arsenal F.C.", None, "England"),
    ("Aston Villa", "Aston Villa F.C.", None, "England"),
    ("Bournemouth", "AFC Bournemouth", None, "England"),
    ("Brentford", "Brentford F.C.", None, "England"),
    ("Brighton", "Brighton & Hove Albion F.C.", None, "England"),
    ("Chelsea", "Chelsea F.C.", None, "England"),
    ("Crystal Palace", "Crystal Palace F.C.", None, "England"),
    ("Everton", "Everton F.C.", None, "England"),
    ("Fulham", "Fulham F.C.", None, "England"),
    ("Ipswich Town", "Ipswich Town F.C.", None, "England"),
    ("Leeds United", "Leeds United F.C.", None, "England"),
    ("Leicester City", "Leicester City F.C.", None, "England"),
    ("Liverpool", "Liverpool F.C.", None, "England"),
    ("Manchester City", "Manchester City F.C.", None, "England"),
    ("Manchester United", "Manchester United F.C.", None, "England"),
    ("Newcastle United", "Newcastle United F.C.", None, "England"),
    ("Nottingham Forest", "Nottingham Forest F.C.", None, "England"),
    ("Southampton", "Southampton F.C.", None, "England"),
    ("Tottenham Hotspur", "Tottenham Hotspur F.C.", None, "England"),
    ("West Ham United", "West Ham United F.C.", None, "England"),
    ("Wolverhampton", "Wolverhampton Wanderers F.C.", None, "England"),
    # Spain
    ("Real Madrid", "Real Madrid CF", None, "Spain"),
    ("Barcelona", "FC Barcelona", None, "Spain"),
    ("Atletico Madrid", "Atlético Madrid", None, "Spain"),
    ("Sevilla", "Sevilla FC", None, "Spain"),
    ("Real Sociedad", "Real Sociedad", None, "Spain"),
    ("Athletic Bilbao", "Athletic Bilbao", None, "Spain"),
    ("Valencia", "Valencia CF", None, "Spain"),
    ("Villarreal", "Villarreal CF", None, "Spain"),
    ("Real Betis", "Real Betis", None, "Spain"),
    # Germany
    ("Bayern Munich", "FC Bayern Munich", None, "Germany"),
    ("Borussia Dortmund", "Borussia Dortmund", None, "Germany"),
    ("RB Leipzig", "RB Leipzig", None, "Germany"),
    ("Bayer Leverkusen", "Bayer 04 Leverkusen", None, "Germany"),
    ("Eintracht Frankfurt", "Eintracht Frankfurt", None, "Germany"),
    ("Schalke 04", "FC Schalke 04", None, "Germany"),
    ("Borussia Monchengladbach", "Borussia Mönchengladbach", None, "Germany"),
    ("VfB Stuttgart", "VfB Stuttgart", None, "Germany"),
    ("Werder Bremen", "SV Werder Bremen", None, "Germany"),
    # Italy
    ("AC Milan", "A.C. Milan", None, "Italy"),
    ("Inter Milan", "Inter Milan", None, "Italy"),
    ("Juventus", "Juventus F.C.", None, "Italy"),
    ("AS Roma", "A.S. Roma", None, "Italy"),
    ("Napoli", "S.S.C. Napoli", None, "Italy"),
    ("Lazio", "S.S. Lazio", None, "Italy"),
    ("Atalanta", "Atalanta BC", None, "Italy"),
    ("Fiorentina", "ACF Fiorentina", None, "Italy"),
    # France
    ("Paris Saint-Germain", "Paris Saint-Germain F.C.", None, "France"),
    ("Olympique Marseille", "Olympique de Marseille", None, "France"),
    ("Olympique Lyonnais", "Olympique Lyonnais", None, "France"),
    ("AS Monaco", "AS Monaco FC", None, "France"),
    ("LOSC Lille", "Lille OSC", None, "France"),
    # Portugal — Liga Portugal
    ("Benfica", "S.L. Benfica", None, "Portugal"),
    ("Porto", "FC Porto", None, "Portugal"),
    ("Sporting CP", "Sporting CP", None, "Portugal"),
    ("Braga", "S.C. Braga", None, "Portugal"),
    ("Vitoria Guimaraes", "Vitória S.C.", None, "Portugal"),
    ("Gil Vicente", "Gil Vicente F.C.", None, "Portugal"),
    ("Boavista", "Boavista F.C.", None, "Portugal"),
    ("Santa Clara", "C.D. Santa Clara", None, "Portugal"),
    ("Moreirense", "Moreirense F.C.", None, "Portugal"),
    ("Famalicao", "F.C. Famalicão", None, "Portugal"),
    ("Arouca", "F.C. Arouca", None, "Portugal"),
    ("Casa Pia", "Casa Pia A.C.", None, "Portugal"),
    ("Estoril", "G.D. Estoril Praia", None, "Portugal"),
    ("Rio Ave", "Rio Ave F.C.", None, "Portugal"),
    ("Estrela Amadora", "C.F. Estrela da Amadora", None, "Portugal"),
    ("Nacional", "C.D. Nacional", None, "Portugal"),
    ("AVS", "AVS Futebol SAD", None, "Portugal"),
    ("Farense", "S.C. Farense", None, "Portugal"),
    # Netherlands
    ("Ajax", "AFC Ajax", None, "Netherlands"),
    ("PSV Eindhoven", "PSV Eindhoven", None, "Netherlands"),
    ("Feyenoord", "Feyenoord", None, "Netherlands"),
    # Belgium
    ("Club Brugge", "Club Brugge KV", None, "Belgium"),
    ("Anderlecht", "R.S.C. Anderlecht", None, "Belgium"),
    # Scotland
    ("Celtic", "Celtic F.C.", None, "Scotland"),
    ("Rangers", "Rangers F.C.", None, "Scotland"),
    # Turkey
    ("Galatasaray", "Galatasaray S.K. (football)", None, "Turkey"),
    ("Fenerbahce", "Fenerbahçe S.K. (football)", None, "Turkey"),
    ("Besiktas", "Beşiktaş J.K.", None, "Turkey"),
    # Greece
    ("Olympiacos", "Olympiacos F.C.", None, "Greece"),
    ("Panathinaikos", "Panathinaikos F.C.", None, "Greece"),
    ("AEK Athens", "AEK Athens F.C.", None, "Greece"),
    # Switzerland
    ("FC Basel", "FC Basel", None, "Switzerland"),
    ("Young Boys", "BSC Young Boys", None, "Switzerland"),
    # Austria
    ("Red Bull Salzburg", "FC Red Bull Salzburg", None, "Austria"),
    ("Rapid Wien", "SK Rapid Wien", None, "Austria"),
    # Denmark
    # Sweden
    ("Malmo FF", "Malmö FF", None, "Sweden"),
    # Norway
    ("Rosenborg", "Rosenborg BK", None, "Norway"),
    # Czech Republic
    ("Sparta Prague", "AC Sparta Prague", None, "Czech Republic"),
    ("Slavia Prague", "SK Slavia Prague", None, "Czech Republic"),
    # Poland
    ("Legia Warsaw", "Legia Warsaw", None, "Poland"),
    # Croatia
    ("Dinamo Zagreb", "GNK Dinamo Zagreb", None, "Croatia"),
    ("Hajduk Split", "HNK Hajduk Split", None, "Croatia"),
    # Serbia
    ("Red Star Belgrade", "Red Star Belgrade", None, "Serbia"),
    ("Partizan", "FK Partizan", None, "Serbia"),
    # Ukraine
    ("Shakhtar Donetsk", "FC Shakhtar Donetsk", None, "Ukraine"),
    ("Dynamo Kyiv", "FC Dynamo Kyiv", None, "Ukraine"),
    # Russia
    ("Spartak Moscow", "FC Spartak Moscow", None, "Russia"),
    ("CSKA Moscow", "PFC CSKA Moscow", None, "Russia"),
    ("Zenit St Petersburg", "FC Zenit Saint Petersburg", None, "Russia"),
    # Romania
    ("Steaua Bucharest", "FCSB", None, "Romania"),
    # Hungary
    ("Ferencvaros", "Ferencvárosi TC", None, "Hungary"),
    # South America
    ("Boca Juniors", "Boca Juniors", None, "Argentina"),
    ("River Plate", "Club Atlético River Plate", None, "Argentina"),
    ("Flamengo", "CR Flamengo", None, "Brazil"),
    ("Santos", "Santos FC", None, "Brazil"),
    ("Palmeiras", "SE Palmeiras", None, "Brazil"),
    ("Corinthians", "Sport Club Corinthians Paulista", None, "Brazil"),
    ("Sao Paulo", "São Paulo FC", None, "Brazil"),
    # Mexico
    ("Club America", "Club América", None, "Mexico"),
    ("Chivas", "C.D. Guadalajara", None, "Mexico"),
]

NBA_TEAMS = [
    # Eastern Conference - Atlantic
    ("Boston Celtics", "Boston Celtics", None, "Eastern"),
    ("Brooklyn Nets", "Brooklyn Nets", None, "Eastern"),
    ("New York Knicks", "New York Knicks", None, "Eastern"),
    ("Philadelphia 76ers", "Philadelphia 76ers", None, "Eastern"),
    ("Toronto Raptors", "Toronto Raptors", None, "Eastern"),
    # Eastern Conference - Central
    ("Chicago Bulls", "Chicago Bulls", None, "Eastern"),
    ("Cleveland Cavaliers", "Cleveland Cavaliers", None, "Eastern"),
    ("Detroit Pistons", "Detroit Pistons", None, "Eastern"),
    ("Indiana Pacers", "Indiana Pacers", None, "Eastern"),
    ("Milwaukee Bucks", "Milwaukee Bucks", None, "Eastern"),
    # Eastern Conference - Southeast
    ("Atlanta Hawks", "Atlanta Hawks", None, "Eastern"),
    ("Charlotte Hornets", "Charlotte Hornets", None, "Eastern"),
    ("Miami Heat", "Miami Heat", None, "Eastern"),
    ("Orlando Magic", "Orlando Magic", None, "Eastern"),
    ("Washington Wizards", "Washington Wizards", None, "Eastern"),
    # Western Conference - Northwest
    ("Denver Nuggets", "Denver Nuggets", None, "Western"),
    ("Minnesota Timberwolves", "Minnesota Timberwolves", None, "Western"),
    ("Oklahoma City Thunder", "Oklahoma City Thunder", None, "Western"),
    ("Portland Trail Blazers", "Portland Trail Blazers", None, "Western"),
    ("Utah Jazz", "Utah Jazz", None, "Western"),
    # Western Conference - Pacific
    ("Golden State Warriors", "Golden State Warriors", None, "Western"),
    ("LA Clippers", "Los Angeles Clippers", None, "Western"),
    ("Los Angeles Lakers", "Los Angeles Lakers", None, "Western"),
    ("Phoenix Suns", "Phoenix Suns", None, "Western"),
    ("Sacramento Kings", "Sacramento Kings", None, "Western"),
    # Western Conference - Southwest
    ("Dallas Mavericks", "Dallas Mavericks", None, "Western"),
    ("Houston Rockets", "Houston Rockets", None, "Western"),
    ("Memphis Grizzlies", "Memphis Grizzlies", None, "Western"),
    ("New Orleans Pelicans", "New Orleans Pelicans", None, "Western"),
    ("San Antonio Spurs", "San Antonio Spurs", None, "Western"),
]

OLYMPICS_ALL = [e[0] for e in OLYMPICS]
WORLD_CUPS_ALL = [e[0] for e in WORLD_CUPS]
EUROS_ALL = [e[0] for e in EUROS]
SPORTS_ALL = [e[0] for e in SPORTS]
FOOTBALL_CLUBS_ALL = [e[0] for e in FOOTBALL_CLUBS]
NBA_TEAMS_ALL = [e[0] for e in NBA_TEAMS]

# Lookup dicts
_ALL_EVENTS = OLYMPICS + WORLD_CUPS + EUROS + SPORTS + FOOTBALL_CLUBS + NBA_TEAMS
WIKIPEDIA = {e[0]: e[1] for e in _ALL_EVENTS}
IMAGE_FILES = {e[0]: e[2] for e in _ALL_EVENTS}
TAGS = {e[0]: e[3] for e in _ALL_EVENTS}
