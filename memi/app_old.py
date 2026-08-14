import logging
import random
import subprocess

import requests as http_requests
from flask import Flask, Response, jsonify, render_template, request

from memi.categories import CATEGORIES
from memi.categories.albums import (
    ARTISTS as ALBUM_ARTISTS,
    MBIDS as ALBUM_MBIDS,
    YEARS as ALBUM_YEARS,
)
from memi.categories.animals import (
    CLASSES as ANIMAL_CLASSES,
    DIFFICULTY as ANIMAL_DIFFICULTY,
)
from memi.categories.brands import BRAND_TAGS
from memi.categories.countries import (
    CONTINENTS as COUNTRY_CONTINENTS,
    DIFFICULTY as COUNTRY_DIFFICULTY,
)
from memi.categories.dinosaurs import ALL as DINOSAUR_LIST
from memi.categories.instruments import FAMILIES as INSTRUMENT_FAMILIES
from memi.categories.logos import LOGOS
from memi.categories.monuments import (
    CONTINENTS as MONUMENT_CONTINENTS,
    DIFFICULTY as MONUMENT_DIFFICULTY,
    LOCATIONS as MONUMENT_LOCATIONS,
)
from memi.categories.movies import YEARS as MOVIE_YEARS
from memi.categories.nature import (
    CONTINENTS as LANDSCAPE_CONTINENTS,
    LOCATIONS as NATURE_LOCATIONS,
)
from memi.categories.paintings import MOVEMENT_PERIODS, PAINTING_INFO
from memi.categories.people import ROLES as PEOPLE_ROLES
from memi.categories.rivers import (
    CONTINENTS as RIVER_CONTINENTS,
    LOCATIONS as RIVER_LOCATIONS,
)
from memi.categories.roadsigns import (
    COMMONS_FILES as SIGN_FILES,
    REGIONS as SIGN_REGIONS,
)
from memi.categories.scientific_names import SCIENTIFIC_NAMES
from memi.categories.space import LOCATIONS as SPACE_LOCATIONS
from memi.categories.sports import (
    IMAGE_FILES as SPORT_IMAGE_FILES,
    TAGS as SPORT_TAGS,
    WIKIPEDIA as SPORT_WIKIPEDIA,
)
from memi.categories.tvshows import YEARS as TV_YEARS
from memi.categories.usstates import REGIONS as STATE_REGIONS
from memi.logic.images import (
    BONES_API_URL,
    get_album_cover,
    get_bone_image,
    get_commons_file_image,
    get_country_item,
    get_dino_image,
    get_fandom_image,
    get_grays_anatomy_image,
    get_logo_image,
    get_state_item,
    get_tmdb_image,
    get_tmdb_tv_image,
    get_wikipedia_description,
    get_wikipedia_file_image,
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

# Load excluded items (approved reports)
EXCLUDED_FILE = "excluded_items.txt"
_excluded_items = set()
try:
    with open(EXCLUDED_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                _excluded_items.add(line)
except FileNotFoundError:
    pass

# Fandom wikis for character categories
FANDOM_WIKIS = {
    "culture:cinema:characters:star wars": "starwars",
    "culture:cinema:characters:lord of the rings": "lotr",
    "culture:cinema:characters:harry potter": "harrypotter",
    "culture:cinema:characters:disney": "disney",
    "culture:cinema:characters:marvel": "marvel",
    "culture:cinema:characters:dc": "dc",
    "culture:cinema:characters:anime": None,
    "culture:cinema:characters:all": None,
}


app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 86400  # 1 day for static files

# Git commit hash for version display
try:
    GIT_VERSION = (
        subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
        )
        .decode()
        .strip()
    )
except Exception:
    GIT_VERSION = "dev"


@app.route("/")
def index():
    top_level, subs = build_menu()
    return render_template(
        "index.html", top_level=top_level, subcategories=subs, version=GIT_VERSION
    )


@app.route("/about")
def about():
    return render_template("about.html", version=GIT_VERSION)


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

    # Filter by continents if provided
    continents_param = request.args.get("continents", "")
    if continents_param:
        continent_map = None
        if category.startswith("geography:countries:"):
            continent_map = COUNTRY_CONTINENTS
        elif category == "culture:art:monuments":
            continent_map = MONUMENT_CONTINENTS
        elif category == "nature:landscapes":
            continent_map = LANDSCAPE_CONTINENTS
        elif category == "geography:rivers":
            continent_map = RIVER_CONTINENTS
        if continent_map:
            allowed = set()
            for c in continents_param.split(","):
                allowed.update(continent_map.get(c, []))
            items = [i for i in items if i in allowed]
            if not items:
                return jsonify({"error": "No items for selected continents"}), 400

    # Filter by animal classes if provided
    classes_param = request.args.get("classes", "")
    if classes_param and category == "nature:animals":
        allowed = set()
        for c in classes_param.split(","):
            allowed.update(ANIMAL_CLASSES.get(c, []))
        items = [i for i in items if i in allowed]
        if not items:
            return jsonify({"error": "No animals for selected classes"}), 400

    # Filter by difficulty if provided
    difficulty_param = request.args.get("difficulty", "")
    if difficulty_param:
        diff_map = None
        if category == "nature:animals":
            diff_map = ANIMAL_DIFFICULTY
        elif category.startswith("geography:countries:"):
            diff_map = COUNTRY_DIFFICULTY
        elif category == "culture:art:monuments":
            diff_map = MONUMENT_DIFFICULTY
        if diff_map:
            allowed = set()
            for d in difficulty_param.split(","):
                allowed.update(diff_map.get(d, []))
            items = [i for i in items if i in allowed]
            if not items:
                return jsonify({"error": "No items for selected difficulty"}), 400

    # Filter by people roles if provided
    roles_param = request.args.get("roles", "")
    if roles_param and category == "humans:people":
        allowed = set()
        for r in roles_param.split(","):
            allowed.update(PEOPLE_ROLES.get(r, []))
        items = [i for i in items if i in allowed]
        if not items:
            return jsonify({"error": "No people for selected roles"}), 400

    # Filter by instrument families if provided
    families_param = request.args.get("families", "")
    if families_param and category == "culture:music:instruments":
        allowed = set()
        for f in families_param.split(","):
            allowed.update(INSTRUMENT_FAMILIES.get(f, []))
        items = [i for i in items if i in allowed]
        if not items:
            return jsonify({"error": "No instruments for selected families"}), 400

    # Filter by US state regions if provided
    if continents_param and category.startswith("geography:us states:"):
        allowed = set()
        for r in continents_param.split(","):
            allowed.update(STATE_REGIONS.get(r, []))
        items = [i for i in items if i in allowed]
        if not items:
            return jsonify({"error": "No states for selected regions"}), 400

    items = [i for i in items if i not in _excluded_items]
    unseen = [i for i in items if i not in seen]
    if not unseen:
        return jsonify({"error": "All items seen"}), 400
    candidates = random.sample(unseen, min(10, len(unseen)))

    is_country = category.startswith("geography:countries:")
    is_us_state = category.startswith("geography:us states:")
    mode = category.split(":")[-1] if (is_country or is_us_state) else None
    is_bones = category == "humans:bones"
    is_road_signs = category == "geography:road signs"
    is_albums = category == "culture:music:albums"
    is_sports = category.startswith("culture:sports:")
    is_brands = category.startswith("culture:brands:")

    is_people = category == "humans:people" or category in (
        "culture:cinema:actors",
        "culture:cinema:directors",
    )
    is_logo = category == "logos"
    is_movie = category.startswith("culture:cinema:movies:")
    movie_mode = category.split(":")[-1] if is_movie else None
    is_tv = category == "culture:cinema:tv shows:scenes"
    is_anatomy = category.startswith("anatomy:")
    fandom_wiki = FANDOM_WIKIS.get(category)

    for item in candidates:
        result = None
        if is_albums:
            mbid = ALBUM_MBIDS.get(item)
            result = get_album_cover(item, mbid)
        elif is_sports:
            if item in LOGOS:
                result = {"name": item, "image": LOGOS[item]}
            else:
                image_file = SPORT_IMAGE_FILES.get(item)
                if image_file:
                    result = get_wikipedia_file_image(image_file)
                if not result or not result.get("image"):
                    wiki = SPORT_WIKIPEDIA.get(item, item)
                    result = get_wikipedia_image(wiki)
        elif is_brands:
            if item in LOGOS:
                result = {"name": item, "image": LOGOS[item]}
        elif is_bones:
            result = get_bone_image(item)
        elif is_road_signs:
            commons_file = SIGN_FILES.get(item)
            if commons_file:
                result = get_commons_file_image(commons_file)
        elif is_us_state:
            result = get_state_item(item, mode)
        elif is_country:
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
        elif item in DINOSAUR_LIST:
            result = get_dino_image(item)
            if not result or not result.get("image"):
                result = get_wikipedia_image(item)
        else:
            result = get_wikipedia_image(item)

        if result and result.get("image"):
            result["item"] = item
            name = result["name"]
            if "(" in name:
                name = name.split("(")[0].strip()
            # Strip trailing " dog" from breed names like "Maltese dog"
            name = name.removesuffix(" dog")
            result["name"] = name
            if is_people:
                desc = get_wikipedia_description(item)
                if desc:
                    desc = desc.replace("(born ", "(").replace("(", "").replace(")", "")
                    result["tag"] = desc
            elif (
                category == "culture:art:paintings:movements"
                and item in MOVEMENT_PERIODS
            ):
                result["tag"] = MOVEMENT_PERIODS[item]
            elif (
                category == "culture:art:paintings:paintings" and item in PAINTING_INFO
            ):
                result["tag"] = PAINTING_INFO[item]
            elif is_tv and item in TV_YEARS:
                result["tag"] = TV_YEARS[item]
            elif is_movie and item in MOVIE_YEARS:
                result["tag"] = MOVIE_YEARS[item]
            elif category == "culture:art:monuments" and item in MONUMENT_LOCATIONS:
                result["tag"] = MONUMENT_LOCATIONS[item]
            elif category == "geography:rivers" and item in RIVER_LOCATIONS:
                result["tag"] = RIVER_LOCATIONS[item]
            elif category.startswith("nature:space") and item in SPACE_LOCATIONS:
                result["tag"] = SPACE_LOCATIONS[item]
            elif category == "nature:animals" or category.startswith("nature:plants:"):
                sci_name = SCIENTIFIC_NAMES.get(item, "")
                display_name = result["name"].lower()
                if sci_name and sci_name.lower() != display_name:
                    result["tag"] = sci_name
            elif category == "nature:landscapes" and item in NATURE_LOCATIONS:
                result["tag"] = NATURE_LOCATIONS[item]
            elif is_road_signs and item in SIGN_REGIONS and SIGN_REGIONS[item]:
                result["tag"] = SIGN_REGIONS[item]
            elif is_albums and item in ALBUM_ARTISTS:
                result["tag"] = f"{ALBUM_ARTISTS[item]} {ALBUM_YEARS.get(item, '')}"
            elif is_sports and item in SPORT_TAGS:
                result["tag"] = SPORT_TAGS[item]
            elif is_brands and item in BRAND_TAGS:
                result["tag"] = BRAND_TAGS[item]
            if is_sports or is_brands:
                result["name"] = item
            if is_road_signs:
                result["name"] = item
            if is_sports or is_road_signs or is_brands:
                result["light_bg"] = True
            return jsonify(result)
        else:
            _fail_logger.warning("FAILED: %s (category: %s)", item, category)

    return jsonify({"error": "No image found"}), 404


@app.route("/api/bones/image/<bone_id>")
def bones_image(bone_id):
    """Proxy bone images from the Bones API."""
    try:
        resp = http_requests.get(
            f"{BONES_API_URL}/bones/{bone_id}",
            timeout=10,
        )
        if resp.status_code != 200:
            return "Not found", 404
        data = resp.json()
        image_path = data.get("image")
        if not image_path:
            return "Not found", 404
        img_resp = http_requests.get(
            f"{BONES_API_URL}{image_path}",
            timeout=10,
        )
        if img_resp.status_code != 200:
            return "Not found", 404
        return Response(
            img_resp.content,
            content_type=img_resp.headers.get("content-type", "image/jpeg"),
        )
    except Exception:
        return "Not found", 404


@app.route("/api/report", methods=["POST"])
def report_item():
    data = request.json or {}
    item = data.get("item", "unknown")
    cats = data.get("cats", "unknown")
    _report_logger.info("REPORTED: %s (categories: %s)", item, cats)
    return jsonify({"ok": True})


@app.route("/review")
def review_reports():
    """Review page for reported items."""
    pending = []
    seen = set()
    try:
        with open("reported_items.log") as f:
            for line in f:
                if "REPORTED:" in line:
                    item = line.split("REPORTED:")[1].split("(categories:")[0].strip()
                    cats = line.split("(categories:")[1].rstrip(")\n").strip()
                    ts = line.split(" REPORTED:")[0].strip()
                    if item not in seen:
                        seen.add(item)
                        status = "excluded" if item in _excluded_items else "pending"
                        pending.append(
                            {"item": item, "cats": cats, "time": ts, "status": status}
                        )
    except FileNotFoundError:
        pass
    return render_template("review.html", reports=pending)


@app.route("/api/review/preview")
def preview_item():
    """Get the image URL for a reported item."""
    item = request.args.get("item", "")
    cats = request.args.get("cats", "")
    if not item or not cats:
        return jsonify({"error": "Missing item or cats"}), 400
    cat = cats.split(",")[0]
    if cat not in CATEGORIES:
        return jsonify({"error": "Unknown category"}), 400

    # Reuse the same image logic as random_item
    category = cat
    is_bones = category == "humans:bones"
    is_road_signs = category == "geography:road signs"
    is_albums = category == "culture:music:albums"
    is_sports = category.startswith("culture:sports:")
    is_brands = category.startswith("culture:brands:")
    is_country = category.startswith("geography:countries:")
    is_us_state = category.startswith("geography:us states:")
    mode = category.split(":")[-1] if (is_country or is_us_state) else None
    fandom_wiki = FANDOM_WIKIS.get(category)

    result = None
    if is_albums:
        mbid = ALBUM_MBIDS.get(item)
        result = get_album_cover(item, mbid)
    elif is_sports:
        if item in LOGOS:
            result = {"name": item, "image": LOGOS[item]}
        else:
            image_file = SPORT_IMAGE_FILES.get(item)
            if image_file:
                result = get_wikipedia_file_image(image_file)
            if not result or not result.get("image"):
                wiki = SPORT_WIKIPEDIA.get(item, item)
                result = get_wikipedia_image(wiki)
    elif is_brands:
        if item in LOGOS:
            result = {"name": item, "image": LOGOS[item]}
    elif is_bones:
        result = get_bone_image(item)
    elif is_road_signs:
        from memi.categories.roadsigns import COMMONS_FILES as SF

        cf = SF.get(item)
        if cf:
            result = get_commons_file_image(cf)
    elif is_us_state:
        result = get_state_item(item, mode)
    elif is_country:
        result = get_country_item(item, mode)
    elif fandom_wiki:
        result = get_fandom_image(item, fandom_wiki)
    if not result or not result.get("image"):
        result = get_wikipedia_image(item)

    if result and result.get("image"):
        return jsonify({"image": result["image"]})
    return jsonify({"error": "No image found"}), 404


@app.route("/api/review/exclude", methods=["POST"])
def exclude_item():
    """Approve a report — exclude item from rotation."""
    data = request.json or {}
    item = data.get("item", "")
    if item:
        _excluded_items.add(item)
        with open(EXCLUDED_FILE, "a") as f:
            f.write(item + "\n")
    return jsonify({"ok": True})


@app.route("/api/review/restore", methods=["POST"])
def restore_item():
    """Dismiss a report — restore item to rotation."""
    data = request.json or {}
    item = data.get("item", "")
    if item:
        _excluded_items.discard(item)
        # Rewrite file without this item
        with open(EXCLUDED_FILE, "w") as f:
            f.writelines(i + "\n" for i in _excluded_items)
    return jsonify({"ok": True})
