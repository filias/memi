import logging
import random
from urllib.parse import quote

import requests
from flask import Flask, jsonify, render_template, request

from memi.categories import CATEGORIES
from memi.categories.countries import CAPITALS
from memi.categories.people import ATHLETE_SPORTS

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
    "characters:star wars": "starwars",
    "characters:lord of the rings": "lotr",
    "characters:harry potter": "harrypotter",
    "characters:disney": "disney",
    "characters:marvel": "marvel",
    "characters:dc": "dc",
    "characters:anime": None,  # no single wiki, use Wikipedia
    "characters:all": None,
}


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


@app.route("/")
def index():
    categories = []
    subs = {}
    for key in CATEGORIES:
        if ":" in key:
            cat, mode = key.split(":", 1)
            subs.setdefault(cat, []).append({"key": key, "label": mode})
        else:
            categories.append({"key": key, "label": key})
    categories.sort(key=lambda c: c["label"])
    subs = dict(sorted(subs.items()))
    for cat in subs:
        subs[cat].sort(key=lambda s: s["label"])
    return render_template("index.html", categories=categories, subcategories=subs)


@app.route("/api/random")
def random_item():
    cats = request.args.get("cats", "")
    cat_list = [c for c in cats.split(",") if c in CATEGORIES]
    if not cat_list:
        return jsonify({"error": "Unknown category"}), 400

    # Pick a random category, then a random item from it
    category = random.choice(cat_list)
    items = CATEGORIES[category]
    candidates = random.sample(items, min(10, len(items)))

    is_country = category.startswith("countries:")
    mode = category.split(":")[1] if is_country else None

    is_athlete = category.startswith("people:athlete")
    is_logo = category == "logos"
    fandom_wiki = FANDOM_WIKIS.get(category)

    for item in candidates:
        result = None
        if is_country:
            result = get_country_item(item, mode)
        elif is_logo:
            result = get_logo_image(item)
        elif fandom_wiki:
            result = get_fandom_image(item, fandom_wiki)
            if not result or not result.get("image"):
                result = get_wikipedia_image(item)
        else:
            result = get_wikipedia_image(item)

        if result and result.get("image"):
            if is_athlete and item in ATHLETE_SPORTS:
                result["tag"] = ATHLETE_SPORTS[item]
            return jsonify(result)
        else:
            _fail_logger.warning("FAILED: %s (category: %s)", item, category)

    return jsonify({"error": "No image found"}), 404
