import random

import requests
from flask import Flask, jsonify, render_template

from memi.categories import CATEGORIES

app = Flask(__name__)

HEADERS = {"User-Agent": "Memi/1.0"}


def get_wikipedia_image(title):
    """Fetch the main image for a Wikipedia article."""
    resp = requests.get(
        "https://en.wikipedia.org/api/rest_v1/page/summary/" + title,
        headers=HEADERS,
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    data = resp.json()
    thumbnail = data.get("thumbnail", {})
    return {
        "name": data.get("title", title),
        "image": thumbnail.get("source"),
    }


@app.route("/")
def index():
    return render_template("index.html", categories=list(CATEGORIES.keys()))


@app.route("/api/random/<category>")
def random_item(category):
    if category not in CATEGORIES:
        return jsonify({"error": "Unknown category"}), 400

    items = CATEGORIES[category]
    candidates = random.sample(items, min(10, len(items)))

    for item in candidates:
        result = get_wikipedia_image(item)
        if result and result["image"]:
            return jsonify(result)

    return jsonify({"error": "No image found"}), 404
