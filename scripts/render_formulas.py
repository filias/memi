"""Render each formula's LaTeX to an SVG in memi/static/img/formulas/.

Run from the repo root:

    uv run --with matplotlib python scripts/render_formulas.py

Re-run after adding/editing formulas in memi/categories/formulas.py.
"""

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from memi.categories.formulas import FORMULAS, slug

OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "memi" / "static" / "img" / "formulas"
GLYPH_COLOR = "#1a2233"  # dark, reads on the light card background


def render(latex: str, path: pathlib.Path) -> None:
    fig = plt.figure(figsize=(6, 2))
    fig.text(
        0.5,
        0.5,
        f"${latex}$",
        fontsize=38,
        ha="center",
        va="center",
        color=GLYPH_COLOR,
    )
    fig.savefig(path, format="svg", bbox_inches="tight", pad_inches=0.25, transparent=True)
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed = []
    for name, data in FORMULAS.items():
        path = OUT_DIR / f"{slug(name)}.svg"
        try:
            render(data["latex"], path)
        # Deliberately broad: mathtext raises assorted types for a bad formula,
        # and one bad formula should not stop the rest of the batch rendering.
        except Exception as exc:  # noqa: BLE001
            failed.append((name, str(exc)))
    print(f"Rendered {len(FORMULAS) - len(failed)}/{len(FORMULAS)} formulas to {OUT_DIR}")
    for name, err in failed:
        print(f"  FAILED: {name}: {err}")


if __name__ == "__main__":
    main()
