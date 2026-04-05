import logging
import random

from flask import Flask, jsonify, render_template, request

from memi.categories import CATEGORIES
from memi.categories.countries import CONTINENTS
from memi.categories.monuments import LOCATIONS as MONUMENT_LOCATIONS
from memi.categories.movies import YEARS as MOVIE_YEARS
from memi.categories.tvshows import YEARS as TV_YEARS
from memi.categories.paintings import MOVEMENT_PERIODS, PAINTING_INFO
from memi.categories.nature import LOCATIONS as NATURE_LOCATIONS
from memi.categories.space import LOCATIONS as SPACE_LOCATIONS
from memi.categories.rivers import LOCATIONS as RIVER_LOCATIONS
from memi.logic.images import (
    get_country_item,
    get_fandom_image,
    get_grays_anatomy_image,
    get_logo_image,
    get_scientific_name,
    get_tmdb_image,
    get_tmdb_tv_image,
    get_wikipedia_description,
    get_wikipedia_image,
)
from memi.logic.menu import build_menu

app = Flask(__name__)

# Log failed image lookups so we can clean up the lists
_fail_logger = logging.getLogger("memi.failed")
_fail_handler = logging.FileHandler("failed_items.log")
_fail_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
_fail_logger.addHandler(_fail_handler)
_fail_logger.setLevel(logging.WARNING)

# Log reported items
_report_logger = logging.getLogger("memi.reports")
_report_handler = logging.FileHandler("reported_items.log")
_report_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
_report_logger.addHandler(_report_handler)
_report_logger.setLevel(logging.INFO)

# Fandom wikis for character categories
FANDOM_WIKIS = {
    "culture:characters:star wars": "starwars",
    "culture:characters:lord of the rings": "lotr",
    "culture:characters:harry potter": "harrypotter",
    "culture:characters:disney": "disney",
    "culture:characters:marvel": "marvel",
    "culture:characters:dc": "dc",
    "culture:characters:anime": None,
    "culture:characters:all": None,
}


@app.route("/")
def index():
    top_level, subs = build_menu()
    return render_template("index.html", top_level=top_level, subcategories=subs)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/api/random")
def random_item():
    cats = request.args.get("cats", "")
    cat_list = [c for c in cats.split(",") if c in CATEGORIES]
    if not cat_list:
        return jsonify({"error": "Unknown category"}), 400

    # Exclude recently seen items
    seen = (
        set(request.args.get("seen", "").split(","))
        if request.args.get("seen")
        else set()
    )

    # Pick a random category, then a random item from it
    category = random.choice(cat_list)
    items = CATEGORIES[category]

    # Filter by continents if provided (countries only)
    continents_param = request.args.get("continents", "")
    if continents_param and category.startswith("geography:countries:"):
        allowed = set()
        for c in continents_param.split(","):
            allowed.update(CONTINENTS.get(c, []))
        items = [i for i in items if i in allowed]
        if not items:
            return jsonify({"error": "No countries for selected continents"}), 400

    unseen = [i for i in items if i not in seen]
    if not unseen:
        unseen = items  # all seen, reset
    candidates = random.sample(unseen, min(10, len(unseen)))

    is_country = category.startswith("geography:countries:")
    mode = category.split(":")[-1] if is_country else None

    is_people = category.startswith("people:") or category in (
        "culture:movies:actors",
        "culture:movies:directors",
    )
    is_logo = category == "logos"
    is_movie = category.startswith("culture:movies:")
    movie_mode = category.split(":")[-1] if is_movie else None
    is_tv = category == "culture:tv shows:scenes"
    is_anatomy = category.startswith("anatomy:")
    fandom_wiki = FANDOM_WIKIS.get(category)

    for item in candidates:
        result = None
        if is_country:
            result = get_country_item(item, mode)
        elif is_tv:
            result = get_tmdb_tv_image(item, "backdrop")
            if not result or not result.get("image"):
                result = get_wikipedia_image(item)
        elif is_movie and movie_mode in ("scenes", "posters"):
            img_type = "backdrop" if movie_mode == "scenes" else "poster"
            result = get_tmdb_image(item, img_type)
            if not result or not result.get("image"):
                result = get_wikipedia_image(item)
        elif is_anatomy:
            result = get_grays_anatomy_image(item)
            if not result or not result.get("image"):
                result = get_wikipedia_image(item)
        elif is_logo:
            result = get_logo_image(item)
        elif fandom_wiki:
            result = get_fandom_image(item, fandom_wiki)
            if not result or not result.get("image"):
                result = get_wikipedia_image(item)
        else:
            result = get_wikipedia_image(item)

        if result and result.get("image"):
            result["item"] = item
            name = result["name"]
            if "(" in name:
                result["name"] = name.split("(")[0].strip()
            if is_people:
                desc = get_wikipedia_description(item)
                if desc:
                    desc = desc.replace("(born ", "(").replace("(", "").replace(")", "")
                    result["tag"] = desc
            elif category == "culture:paintings:movements" and item in MOVEMENT_PERIODS:
                result["tag"] = MOVEMENT_PERIODS[item]
            elif category == "culture:paintings:paintings" and item in PAINTING_INFO:
                result["tag"] = PAINTING_INFO[item]
            elif is_tv and item in TV_YEARS:
                result["tag"] = TV_YEARS[item]
            elif is_movie and item in MOVIE_YEARS:
                result["tag"] = MOVIE_YEARS[item]
            elif category == "culture:monuments" and item in MONUMENT_LOCATIONS:
                result["tag"] = MONUMENT_LOCATIONS[item]
            elif category == "geography:rivers" and item in RIVER_LOCATIONS:
                result["tag"] = RIVER_LOCATIONS[item]
            elif category == "nature:space" and item in SPACE_LOCATIONS:
                result["tag"] = SPACE_LOCATIONS[item]
            elif category.startswith("nature:animals:") or category.startswith(
                "nature:plants:"
            ):
                sci_name = get_scientific_name(item)
                display_name = result["name"].lower()
                if sci_name and sci_name.lower() != display_name:
                    result["tag"] = sci_name
            elif category == "nature:landscapes" and item in NATURE_LOCATIONS:
                result["tag"] = NATURE_LOCATIONS[item]
            return jsonify(result)
        else:
            _fail_logger.warning("FAILED: %s (category: %s)", item, category)

    return jsonify({"error": "No image found"}), 404


@app.route("/api/report", methods=["POST"])
def report_item():
    data = request.json or {}
    item = data.get("item", "unknown")
    cats = data.get("cats", "unknown")
    _report_logger.info("REPORTED: %s (categories: %s)", item, cats)
    return jsonify({"ok": True})
