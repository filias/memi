"""Render each sequence prompt ("2, 3, 5, 7, …, ?") to an SVG.

Run from the repo root:

    uv run --with matplotlib python scripts/render_sequences.py

Re-run after editing memi/categories/sequences.py.
"""

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from memi.categories.sequences import SEQUENCES, prompt_text, slug

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "memi" / "static" / "img" / "sequences"
GLYPH_COLOR = "#1a2233"


def render(text: str, path: pathlib.Path) -> None:
    fig = plt.figure(figsize=(7, 1.6))
    fig.text(0.5, 0.5, text, fontsize=34, ha="center", va="center", color=GLYPH_COLOR)
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.25, transparent=True)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name in SEQUENCES:
        render(prompt_text(name), OUT_DIR / f"{slug(name)}.svg")
    print(f"Rendered {len(SEQUENCES)} sequences to {OUT_DIR}")


if __name__ == "__main__":
    main()
