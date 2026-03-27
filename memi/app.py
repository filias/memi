import logging
import os
import random
from urllib.parse import quote

import requests
from flask import Flask, jsonify, render_template, request

from memi.categories import CATEGORIES
from memi.categories.countries import CAPITALS
from memi.categories.monuments import LOCATIONS as MONUMENT_LOCATIONS
from memi.categories.movies import YEARS as MOVIE_YEARS
from memi.categories.tvshows import YEARS as TV_YEARS
from memi.categories.paintings import MOVEMENT_PERIODS, PAINTING_INFO
from memi.categories.nature import LOCATIONS as NATURE_LOCATIONS
from memi.categories.space import LOCATIONS as SPACE_LOCATIONS
from memi.categories.rivers import LOCATIONS as RIVER_LOCATIONS

app = Flask(__name__)

HEADERS = {"User-Agent": "Memi/1.0"}

# Log failed image lookups so we can clean up the lists
_fail_logger = logging.getLogger("memi.failed")
_fail_handler = logging.FileHandler("failed_items.log")
_fail_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
_fail_logger.addHandler(_fail_handler)
_fail_logger.setLevel(logging.WARNING)

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


def get_wikipedia_description(title):
    """Fetch the short description for a Wikipedia article (e.g. 'German physicist (1879-1955)')."""
    try:
        resp = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + title,
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code == 200:
            return resp.json().get("description", "")
    except Exception:
        pass
    return ""


def get_scientific_name(title):
    """Fetch the scientific/taxon name from Wikidata for a plant or animal."""
    try:
        resp = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={"action": "query", "titles": title, "prop": "pageprops", "format": "json"},
            headers=HEADERS,
            timeout=5,
        )
        if resp.status_code != 200:
            return ""
        pages = resp.json().get("query", {}).get("pages", {})
        wikidata_id = ""
        for p in pages.values():
            wikidata_id = p.get("pageprops", {}).get("wikibase_item", "")
        if not wikidata_id:
            return ""
        resp2 = requests.get(
            "https://www.wikidata.org/w/api.php",
            params={"action": "wbgetclaims", "entity": wikidata_id, "property": "P225", "format": "json"},
            headers=HEADERS,
            timeout=5,
        )
        if resp2.status_code != 200:
            return ""
        claims = resp2.json().get("claims", {}).get("P225", [])
        if claims:
            return claims[0]["mainsnak"]["datavalue"]["value"]
    except Exception:
        pass
    return ""


def get_wikipedia_image(title):
    """Fetch the main image for a Wikipedia article via the pageimages API."""
    resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "titles": title,
            "prop": "pageimages",
            "pithumbsize": 800,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    pages = resp.json().get("query", {}).get("pages", {})
    for page in pages.values():
        thumb = page.get("thumbnail", {}).get("source")
        if thumb:
            return {
                "name": page.get("title", title),
                "image": thumb,
            }
    return None


TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")


def get_tmdb_image(title, image_type="backdrop"):
    """Fetch a movie image from TMDB. image_type: 'backdrop' for scenes, 'poster' for posters."""
    if not TMDB_API_KEY:
        return None
    # Strip disambiguation for search
    search_term = title.split("(")[0].strip()
    try:
        resp = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={"query": search_term},
            headers={"Authorization": f"Bearer {TMDB_API_KEY}"},
            timeout=10,
        )
        if resp.status_code != 200:
            return None
        results = resp.json().get("results", [])
        if not results:
            return None
        movie = results[0]
        path = movie.get("backdrop_path") if image_type == "backdrop" else movie.get("poster_path")
        if not path:
            # Fallback: try the other type
            path = movie.get("poster_path") or movie.get("backdrop_path")
        if not path:
            return None
        size = "w780" if image_type == "backdrop" else "w500"
        return {
            "name": title,
            "image": f"https://image.tmdb.org/t/p/{size}{path}",
        }
    except Exception:
        return None


def get_tmdb_tv_image(title, image_type="backdrop"):
    """Fetch a TV show image from TMDB."""
    if not TMDB_API_KEY:
        return None
    search_term = title.split("(")[0].strip()
    try:
        resp = requests.get(
            "https://api.themoviedb.org/3/search/tv",
            params={"query": search_term},
            headers={"Authorization": f"Bearer {TMDB_API_KEY}"},
            timeout=10,
        )
        if resp.status_code != 200:
            return None
        results = resp.json().get("results", [])
        if not results:
            return None
        show = results[0]
        path = show.get("backdrop_path") if image_type == "backdrop" else show.get("poster_path")
        if not path:
            path = show.get("poster_path") or show.get("backdrop_path")
        if not path:
            return None
        size = "w780" if image_type == "backdrop" else "w500"
        return {
            "name": title,
            "image": f"https://image.tmdb.org/t/p/{size}{path}",
        }
    except Exception:
        return None


def get_grays_anatomy_image(title):
    """Fetch a Gray's Anatomy illustration from Wikimedia Commons."""
    # Strip disambiguation suffixes for search
    search_term = title.split("(")[0].strip()
    resp = requests.get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action": "query",
            "list": "search",
            "srnamespace": 6,
            "srsearch": f'"Gray\'s Anatomy" {search_term} png',
            "srlimit": 5,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    results = resp.json().get("query", {}).get("search", [])
    if not results:
        return None
    # Pick the best match — prefer filenames containing the bone name
    chosen = results[0]["title"]
    for r in results:
        if search_term.lower().split()[0] in r["title"].lower():
            chosen = r["title"]
            break
    # Get the image URL
    resp2 = requests.get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action": "query",
            "titles": chosen,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 500,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp2.status_code != 200:
        return None
    pages = resp2.json().get("query", {}).get("pages", {})
    for page in pages.values():
        if "imageinfo" in page:
            thumb = page["imageinfo"][0].get("thumburl")
            if thumb:
                return {"name": title, "image": thumb}
    return None


def get_fandom_image(title, wiki):
    """Fetch image from a Fandom wiki using the imageserving API."""
    # Strip Wikipedia disambiguation suffixes like "(Star Wars)" or "(character)"
    clean = title.split("(")[0].strip().replace(" ", "_")
    try:
        resp = requests.get(
            f"https://{wiki}.fandom.com/api.php",
            params={
                "action": "imageserving",
                "wisTitle": clean,
                "format": "json",
            },
            headers=HEADERS,
            timeout=10,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        image_url = data.get("image", {}).get("imageserving")
        if image_url:
            return {"name": title, "image": image_url}
    except Exception:
        pass
    return None


def get_river_map(title):
    """Fetch a map/basin image for a river from its Wikipedia article."""
    resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "titles": title,
            "prop": "images",
            "imlimit": 100,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    pages = resp.json().get("query", {}).get("pages", {})
    map_keywords = ["map", "basin", "watershed", "course", "locator"]
    map_files = []
    river_name = title.split("(")[0].replace("River", "").replace("river", "").strip().lower()
    for page in pages.values():
        for img in page.get("images", []):
            fname = img["title"].lower()
            if any(kw in fname for kw in map_keywords) and "commons-logo" not in fname:
                map_files.append(img["title"])
    if not map_files:
        return None
    # Prefer files matching the river name
    chosen = None
    for f in map_files:
        if any(word in f.lower() for word in river_name.split() if len(word) > 2):
            chosen = f
            break
    if not chosen:
        chosen = map_files[0]
    # Get image URL
    resp2 = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "titles": chosen,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 500,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp2.status_code != 200:
        return None
    pages2 = resp2.json().get("query", {}).get("pages", {})
    for page in pages2.values():
        if "imageinfo" in page:
            thumb = page["imageinfo"][0].get("thumburl")
            if thumb:
                return {"name": title, "image": thumb}
    return None


def get_logo_image(title):
    """Fetch the logo image for a company by searching article images."""
    resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "titles": title,
            "prop": "images",
            "imlimit": 50,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    pages = resp.json().get("query", {}).get("pages", {})
    # Collect all logo images, prefer ones matching the company name
    logo_files = []
    name_lower = title.split("(")[0].strip().lower()
    for page in pages.values():
        for img in page.get("images", []):
            fname = img["title"].lower()
            if "logo" in fname and "commons-logo" not in fname:
                logo_files.append(img["title"])
    if not logo_files:
        return None
    # Prefer files whose name contains the company name
    logo_file = None
    for f in logo_files:
        if any(word in f.lower() for word in name_lower.split() if len(word) > 2):
            logo_file = f
            break
    if not logo_file:
        logo_file = logo_files[0]
    if not logo_file:
        return None
    # Get the actual image URL
    resp2 = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "titles": logo_file,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 500,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp2.status_code != 200:
        return None
    pages2 = resp2.json().get("query", {}).get("pages", {})
    for page in pages2.values():
        if "imageinfo" in page:
            thumb = page["imageinfo"][0].get("thumburl")
            if thumb:
                return {"name": title, "image": thumb}
    return None


def get_country_shape(country):
    """Fetch the orthographic projection map for a country."""
    # Most countries have a "{Country} (orthographic projection).svg" on Wikipedia
    filename = f"File:{country} (orthographic projection).svg"
    resp = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "titles": filename,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 500,
            "format": "json",
        },
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        if "imageinfo" in page:
            thumb = page["imageinfo"][0].get("thumburl")
            if thumb:
                return {"name": country, "image": thumb}
    return None


def get_country_item(country, mode):
    """Fetch a country image based on mode (flags, shapes, or capitals)."""
    if mode == "flags":
        result = get_wikipedia_image("Flag of " + country)
        if result and result["image"]:
            result["name"] = country
            return result
    elif mode == "capitals":
        result = get_country_shape(country)
        if result:
            capital = CAPITALS.get(country, "Unknown")
            result["clue"] = country
            result["name"] = capital
            return result
    else:
        return get_country_shape(country)
    return None


def _build_menu():
    """Build a nested menu structure from CATEGORIES keys.

    Returns (top_level, subcategories) where:
    - top_level: sorted list of {"label": ..., "key": ... or "has_submenu": True}
    - subcategories: dict of parent -> list of children
    """
    top_level_keys = set()
    subs = {}

    for key in CATEGORIES:
        parts = key.split(":")
        if len(parts) == 1:
            top_level_keys.add(key)
        elif len(parts) == 2:
            parent, label = parts
            top_level_keys.add(parent)
            subs.setdefault(parent, []).append({"key": key, "label": label})
        elif len(parts) == 3:
            parent, group, label = parts
            top_level_keys.add(parent)
            parent_list = subs.setdefault(parent, [])
            sub_group = None
            for item in parent_list:
                if item.get("label") == group and "children" in item:
                    sub_group = item
                    break
            if not sub_group:
                sub_group = {"label": group, "children": []}
                parent_list.append(sub_group)
            sub_group["children"].append({"key": key, "label": label})

    # Build sorted top-level list
    top_level = []
    for name in sorted(top_level_keys):
        if name in subs:
            top_level.append({"label": name, "has_submenu": True})
        else:
            top_level.append({"label": name, "key": name})

    # Sort subcategories
    for cat in subs:
        for item in subs[cat]:
            if "children" in item:
                item["children"].sort(key=lambda s: (s["label"] != "all", s["label"]))
        subs[cat].sort(key=lambda s: (s.get("label", "") != "all", s.get("label", "")))

    return top_level, subs


@app.route("/")
def index():
    top_level, subs = _build_menu()
    return render_template("index.html", top_level=top_level, subcategories=subs)


@app.route("/api/random")
def random_item():
    cats = request.args.get("cats", "")
    cat_list = [c for c in cats.split(",") if c in CATEGORIES]
    if not cat_list:
        return jsonify({"error": "Unknown category"}), 400

    # Exclude recently seen items
    seen = set(request.args.get("seen", "").split(",")) if request.args.get("seen") else set()

    # Pick a random category, then a random item from it
    category = random.choice(cat_list)
    items = CATEGORIES[category]
    unseen = [i for i in items if i not in seen]
    if not unseen:
        unseen = items  # all seen, reset
    candidates = random.sample(unseen, min(10, len(unseen)))

    is_country = category.startswith("geography:countries:")
    mode = category.split(":")[-1] if is_country else None

    is_people = category.startswith("people:") or category in ("culture:movies:actors", "culture:movies:directors")
    is_logo = category == "logos"
    is_river = category == "geography:rivers"
    is_anatomy = category.startswith("anatomy:")
    is_movie = category.startswith("culture:movies:")
    movie_mode = category.split(":")[-1] if is_movie else None
    is_tv = category == "culture:tv shows:scenes"
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
            result["item"] = item  # original list item for seen tracking
            # Strip Wikipedia disambiguation brackets from display name
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
            elif category.startswith("nature:animals:") or category.startswith("nature:plants:"):
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


# Log reported items
_report_logger = logging.getLogger("memi.reports")
_report_handler = logging.FileHandler("reported_items.log")
_report_handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
_report_logger.addHandler(_report_handler)
_report_logger.setLevel(logging.INFO)


@app.route("/api/report", methods=["POST"])
def report_item():
    data = request.json or {}
    item = data.get("item", "unknown")
    cats = data.get("cats", "unknown")
    _report_logger.info("REPORTED: %s (categories: %s)", item, cats)
    return jsonify({"ok": True})
