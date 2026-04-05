# memi

A memory practice game. Pick a category, look at the image, and try to guess what it is before revealing the answer.

Live at [memi.click](https://memi.click)

## Categories

- **Geography** — countries (capitals, flags, shapes) with continent filters, rivers
- **Nature** — animals, plants, landscapes, space
- **Culture** — movies, TV shows, paintings, monuments, fictional characters
- **People** — scientists, explorers, artists, musicians, writers, leaders, actors, athletes

## Run locally

```
uv run python -m memi
```

Then open http://localhost:8080

Set `TMDB_API_KEY` for movie/TV show images.

## Project structure

```
memi/
├── app.py              # Flask routes
├── logic/
│   ├── images.py       # Image fetching (Wikipedia, TMDB, Fandom)
│   └── menu.py         # Menu builder
├── categories/         # Item lists per category
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    ├── index.html
    └── about.html
```

## Deploy

Pushes to `main` auto-deploy via GitHub webhook.

## Lint

```
uvx ruff check . && uvx ruff format --check .
```
