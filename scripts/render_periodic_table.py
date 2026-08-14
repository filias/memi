"""Render a periodic-table tile (atomic number + symbol) per element to SVG.

Run from the repo root:

    uv run --with matplotlib python scripts/render_periodic_table.py

Re-run after regenerating _periodic_data.py.
"""

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from memi.categories.periodic_table import ELEMENTS, slug

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "memi" / "static" / "img" / "elements"
INK = "#1a2233"


def render(symbol: str, number: int, path: pathlib.Path) -> None:
    fig, ax = plt.subplots(figsize=(2.4, 2.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(Rectangle((0.1, 0.08), 0.8, 0.84, fill=False, lw=3, ec=INK))
    ax.text(0.2, 0.8, str(number), fontsize=22, ha="left", va="center", color=INK)
    ax.text(0.5, 0.42, symbol, fontsize=68, ha="center", va="center", color=INK, fontweight="bold")
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.1, transparent=True)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in ELEMENTS.items():
        render(data["symbol"], data["number"], OUT_DIR / f"{slug(name)}.svg")
    print(f"Rendered {len(ELEMENTS)} element tiles to {OUT_DIR}")


if __name__ == "__main__":
    main()
