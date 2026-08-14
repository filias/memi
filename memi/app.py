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
    default_category="nature:animals",
    title="memi",
    subtitle="practise your memory",
    favicon_color="#0d9488",
    sponsor_url="https://github.com/sponsors/filias",
    sponsor_text="sponsor",
    related_sites=[
        {"name": "memi portugal", "url": "https://pt.memi.click"},
        {"name": "memi lisboa", "url": "https://lx.memi.click"},
        {"name": "memi slovensko", "url": "https://sk.memi.click"},
        {"name": "memi US", "url": "https://us.memi.click"},
    ],
    about_html="""
        <p>I love games and I've always wanted a simple card game that would
        help me learn new things while keeping my memory sharp.</p>
        <p>Memi is that game. Countries, movies, animals, paintings, famous
        people &mdash; there's always something new to learn or remember.</p>

        <h2>How to play</h2>
        <p>Pick a category, look at the image, and try to guess what it is
        before revealing the answer. No accounts, no scores, no pressure
        &mdash; just you and your memory.</p>
        <p>A few helpers sit in the bottom row:</p>
        <ul>
            <li><strong>clues:</strong> toggle progressive letter hints &mdash;
            reveals the first letter, then the next, and so on. Handy when
            the name is on the tip of your tongue.</li>
            <li><strong>know more:</strong> appears on reveal and opens the
            Wikipedia article (or source page) for the item, so you can read
            further.</li>
            <li><strong>report:</strong> flag a card if the image doesn't match
            the answer (wrong picture, broken thumbnail, etc.).</li>
        </ul>
        <p>You can play it two ways:</p>
        <ul>
            <li><strong>To learn:</strong> when you don't recognise an item,
            reveal the answer and follow the <em>know more</em> link to read
            about it. Each exposure strengthens the link between the image
            and the name.</li>
            <li><strong>To test yourself:</strong> once a category feels
            familiar, cycle through it and see how many you can name
            without revealing.</li>
        </ul>

        <h2>Why it works</h2>
        <p>This is a simple form of <em>active recall</em> &mdash; pulling
        information out of memory instead of re-reading it. The
        <em>testing effect</em>, well documented in cognitive psychology,
        shows that retrieval practice builds more durable memory traces
        than re-exposure alone.</p>
        <p>Because each prompt is a picture, the game also leverages the
        <em>picture superiority effect</em>: images are encoded more richly
        than words and are easier to retrieve later. Naming the item is a
        form of <em>cued recall</em>, sitting between simple recognition
        (&ldquo;have I seen this before?&rdquo;) and unaided <em>free
        recall</em>.</p>
        <p>Short, frequent sessions outperform long ones &mdash; the
        <em>spacing effect</em>. A few minutes a day is enough.</p>
    """,
    analytics_html=(
        '<script data-goatcounter="https://memi.goatcounter.com/count"'
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
