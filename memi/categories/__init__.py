from memi.categories import anatomy, animals, characters, countries, directors, logos, monuments, movies, nature, people, plants, rivers

CATEGORIES = {
    # Culture
    "culture:characters:all": characters.ALL,
    "culture:characters:star wars": characters.STAR_WARS,
    "culture:characters:lord of the rings": characters.LORD_OF_THE_RINGS,
    "culture:characters:harry potter": characters.HARRY_POTTER,
    "culture:characters:disney": characters.DISNEY,
    "culture:characters:marvel": characters.MARVEL,
    "culture:characters:dc": characters.DC,
    "culture:characters:anime": characters.ANIME,
    "culture:monuments": monuments.ALL,
    "culture:movies:actors": people.ACTORS,
    "culture:movies:directors": directors.ALL,
    "culture:movies:posters": movies.ALL,
    "culture:movies:scenes": movies.ALL,
    # Geography
    "geography:countries:capitals": countries.ALL,
    "geography:countries:flags": countries.ALL,
    "geography:countries:shapes": countries.ALL,
    "geography:rivers": rivers.ALL,
    # Nature
    "nature:all": animals.ALL + plants.ALL + nature.ALL,
    "nature:animals:all": animals.ALL,
    "nature:animals:mammals": animals.MAMMALS,
    "nature:animals:birds": animals.BIRDS,
    "nature:animals:reptiles": animals.REPTILES,
    "nature:animals:amphibians": animals.AMPHIBIANS,
    "nature:animals:marine": animals.MARINE,
    "nature:animals:insects": animals.INSECTS,
    "nature:landscapes": nature.ALL,
    "nature:plants:all": plants.ALL,
    "nature:plants:flowers": plants.FLOWERS,
    "nature:plants:fruits & vegetables": plants.FRUITS_AND_VEGETABLES,
    "nature:plants:houseplants": plants.HOUSEPLANTS,
    "nature:plants:other": plants.OTHER,
    "nature:plants:trees": plants.TREES,
    # People
    "people:all": people.ALL,
    "people:scientists": people.SCIENTISTS,
    "people:explorers": people.EXPLORERS,
    "people:artists": people.ARTISTS,
    "people:musicians": people.MUSICIANS,
    "people:writers": people.WRITERS,
    "people:leaders": people.LEADERS,
    "people:actors": people.ACTORS,
    "people:athletes": people.ATHLETES,
    # Disabled
    # "anatomy:bones": anatomy.BONES,  # TODO: find better bone image source
    # "logos": logos.ALL,  # TODO: find symbol-only logos without text
}
