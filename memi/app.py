import random
from urllib.parse import quote

import requests
from flask import Flask, jsonify, render_template, request

from memi.categories import CATEGORIES

app = Flask(__name__)

HEADERS = {"User-Agent": "Memi/1.0"}


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
    """Fetch a country image based on mode (flags or shapes)."""
    if mode == "flags":
        result = get_wikipedia_image("Flag of " + country)
        if result and result["image"]:
            result["name"] = country
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

    for item in candidates:
        if is_country:
            result = get_country_item(item, mode)
        else:
            result = get_wikipedia_image(item)
        if result and result.get("image"):
            return jsonify(result)

    return jsonify({"error": "No image found"}), 404
