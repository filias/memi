"""Memi - the global memory card game instance.

This is the entry point that creates the Flask app using memi-engine.
All category-specific logic lives in memi/providers/.
"""

import os

import requests as http_requests
from flask import Response

from memi_engine import MemiConfig, create_app
from memi_engine.images import BONES_API_URL

# Import providers — this registers them in the engine
import memi.providers  # noqa: F401

config = MemiConfig(
    title="memi",
    subtitle="practise your memory",
    sponsor_url="https://github.com/sponsors/filias",
    sponsor_text="sponsor",
    about_html="""
        <p>I love games and I've always wanted a simple card game that would
        help me learn new things while keeping my memory sharp.</p>
        <p>Memi is that game. Pick a category, look at the image, and try to
        guess what it is before revealing the answer. Countries, movies, animals,
        paintings, famous people — there's always something new to learn or
        remember.</p>
        <p>No accounts, no scores, no pressure. Just you and your memory.</p>
    """,
    analytics_html=(
        '<script data-goatcounter="https://filias.goatcounter.com/count"'
        ' async src="//gc.zgo.at/count.js"></script>'
    ),
    footers={
        "tmdb": (
            '<a href="https://www.themoviedb.org/" target="_blank" rel="noopener"'
            ' style="opacity:0.4;"><img src="/static/tmdb-logo.svg" alt="TMDB"'
            ' style="height:1rem;"></a>'
        ),
        "eskeletons": (
            'Bone images courtesy of <a href="https://www.eskeletons.org/"'
            ' target="_blank" rel="noopener"'
            ' style="color:var(--tag-secondary);">eSkeletons.org</a>,'
            " John Kappelman &amp; UT Austin"
            ' (<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/"'
            ' target="_blank" rel="noopener"'
            ' style="color:var(--tag-secondary);">CC BY-NC-SA 4.0</a>)'
        ),
        "musicbrainz": (
            'Album covers from <a href="https://coverartarchive.org/"'
            ' target="_blank" rel="noopener"'
            ' style="color:var(--tag-secondary);">Cover Art Archive</a>'
            ' / <a href="https://musicbrainz.org/" target="_blank"'
            ' rel="noopener" style="color:var(--tag-secondary);">MusicBrainz</a>'
        ),
    },
)

# Create the app with instance static folder for logos etc.
instance_static = os.path.join(os.path.dirname(__file__), "static")
app = create_app(config, instance_static=instance_static)


# Bones image proxy (specific to this instance)
@app.route("/api/bones/image/<bone_id>")
def bones_image(bone_id):
    """Proxy bone images from the Bones API."""
    try:
        resp = http_requests.get(f"{BONES_API_URL}/bones/{bone_id}", timeout=10)
        if resp.status_code != 200:
            return "Not found", 404
        data = resp.json()
        image_path = data.get("image")
        if not image_path:
            return "Not found", 404
        img_resp = http_requests.get(f"{BONES_API_URL}{image_path}", timeout=10)
        if img_resp.status_code != 200:
            return "Not found", 404
        return Response(
            img_resp.content,
            content_type=img_resp.headers.get("content-type", "image/jpeg"),
        )
    except Exception:
        return "Not found", 404
