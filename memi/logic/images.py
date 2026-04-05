import os

import requests

from memi.categories.countries import CAPITALS, CURRENCIES

HEADERS = {"User-Agent": "Memi/1.0"}
TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
BONES_API_URL = os.environ.get("BONES_API_URL", "http://127.0.0.1:8081")


def get_wikipedia_image(title):
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
            return {"name": page.get("title", title), "image": thumb}
    return None


def get_wikipedia_description(title):
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
    try:
        resp = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "titles": title,
                "prop": "pageprops",
                "format": "json",
            },
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
            params={
                "action": "wbgetclaims",
                "entity": wikidata_id,
                "property": "P225",
                "format": "json",
            },
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


def get_tmdb_image(title, image_type="backdrop"):
    if not TMDB_API_KEY:
        return None
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
        path = (
            movie.get("backdrop_path")
            if image_type == "backdrop"
            else movie.get("poster_path")
        )
        if not path:
            path = movie.get("poster_path") or movie.get("backdrop_path")
        if not path:
            return None
        size = "w780" if image_type == "backdrop" else "w500"
        return {"name": title, "image": f"https://image.tmdb.org/t/p/{size}{path}"}
    except Exception:
        return None


def get_tmdb_tv_image(title, image_type="backdrop"):
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
        path = (
            show.get("backdrop_path")
            if image_type == "backdrop"
            else show.get("poster_path")
        )
        if not path:
            path = show.get("poster_path") or show.get("backdrop_path")
        if not path:
            return None
        size = "w780" if image_type == "backdrop" else "w500"
        return {"name": title, "image": f"https://image.tmdb.org/t/p/{size}{path}"}
    except Exception:
        return None


def get_grays_anatomy_image(title):
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
    chosen = results[0]["title"]
    for r in results:
        if search_term.lower().split()[0] in r["title"].lower():
            chosen = r["title"]
            break
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
    clean = title.split("(")[0].strip().replace(" ", "_")
    try:
        resp = requests.get(
            f"https://{wiki}.fandom.com/api.php",
            params={"action": "imageserving", "wisTitle": clean, "format": "json"},
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
    river_name = (
        title.split("(")[0].replace("River", "").replace("river", "").strip().lower()
    )
    for page in pages.values():
        for img in page.get("images", []):
            fname = img["title"].lower()
            if any(kw in fname for kw in map_keywords) and "commons-logo" not in fname:
                map_files.append(img["title"])
    if not map_files:
        return None
    chosen = None
    for f in map_files:
        if any(word in f.lower() for word in river_name.split() if len(word) > 2):
            chosen = f
            break
    if not chosen:
        chosen = map_files[0]
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
    logo_files = []
    name_lower = title.split("(")[0].strip().lower()
    for page in pages.values():
        for img in page.get("images", []):
            fname = img["title"].lower()
            if "logo" in fname and "commons-logo" not in fname:
                logo_files.append(img["title"])
    if not logo_files:
        return None
    logo_file = None
    for f in logo_files:
        if any(word in f.lower() for word in name_lower.split() if len(word) > 2):
            logo_file = f
            break
    if not logo_file:
        logo_file = logo_files[0]
    if not logo_file:
        return None
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
    pages = resp.json().get("query", {}).get("pages", {})
    for page in pages.values():
        if "imageinfo" in page:
            thumb = page["imageinfo"][0].get("thumburl")
            if thumb:
                return {"name": country, "image": thumb}
    return None


def get_country_item(country, mode):
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
    elif mode == "currencies":
        result = get_country_shape(country)
        if result:
            currency = CURRENCIES.get(country, "Unknown")
            result["clue"] = country
            currency_name = currency.split("(")[0].strip()
            result["name"] = currency_name
            # Show currency code as tag
            if "(" in currency:
                result["tag"] = currency.split("(")[1].rstrip(")")
            # Fetch coin/note image from Wikipedia
            img = get_wikipedia_image(currency_name)
            if img and img.get("image"):
                result["reveal_image"] = img["image"]
            return result
    else:
        return get_country_shape(country)
    return None


def get_bone_image(bone_id):
    """Fetch a bone image from the Bones API."""
    try:
        resp = requests.get(
            f"{BONES_API_URL}/bones/{bone_id}",
            timeout=10,
        )
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not data.get("has_image"):
            return None
        return {
            "name": data["name"],
            "image": f"/api/bones/image/{bone_id}",
            "tag": data.get("region", ""),
        }
    except Exception:
        return None
