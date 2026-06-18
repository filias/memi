"""Number sequences for the Science category.

The card shows the first terms followed by "?"; the answer is the next
term, and the sequence's name is revealed as a tag. `kind` is the filter.
SVGs are pre-rendered by scripts/render_sequences.py.
"""

import re

SEQUENCES = {
    # Arithmetic
    "Even numbers": {"terms": [2, 4, 6, 8, 10, 12], "next": 14, "kind": "arithmetic"},
    "Odd numbers": {"terms": [1, 3, 5, 7, 9, 11], "next": 13, "kind": "arithmetic"},
    "Multiples of 3": {"terms": [3, 6, 9, 12, 15, 18], "next": 21, "kind": "arithmetic"},
    # Geometric
    "Powers of 2": {"terms": [1, 2, 4, 8, 16, 32], "next": 64, "kind": "geometric"},
    "Powers of 3": {"terms": [1, 3, 9, 27, 81, 243], "next": 729, "kind": "geometric"},
    "Powers of 4": {"terms": [1, 4, 16, 64, 256], "next": 1024, "kind": "geometric"},
    "Powers of 10": {"terms": [1, 10, 100, 1000, 10000], "next": 100000, "kind": "geometric"},
    # Figurate
    "Square numbers": {"terms": [1, 4, 9, 16, 25, 36], "next": 49, "kind": "figurate"},
    "Triangular numbers": {"terms": [1, 3, 6, 10, 15, 21], "next": 28, "kind": "figurate"},
    "Cube numbers": {"terms": [1, 8, 27, 64, 125], "next": 216, "kind": "figurate"},
    "Pentagonal numbers": {"terms": [1, 5, 12, 22, 35, 51], "next": 70, "kind": "figurate"},
    "Tetrahedral numbers": {"terms": [1, 4, 10, 20, 35, 56], "next": 84, "kind": "figurate"},
    "Hexagonal numbers": {"terms": [1, 6, 15, 28, 45, 66], "next": 91, "kind": "figurate"},
    # Recursive
    "Fibonacci numbers": {"terms": [1, 1, 2, 3, 5, 8, 13], "next": 21, "kind": "recursive"},
    "Lucas numbers": {"terms": [2, 1, 3, 4, 7, 11, 18], "next": 29, "kind": "recursive"},
    "Pell numbers": {"terms": [0, 1, 2, 5, 12, 29], "next": 70, "kind": "recursive"},
    "Tribonacci numbers": {"terms": [0, 1, 1, 2, 4, 7, 13], "next": 24, "kind": "recursive"},
    # Famous / number theory
    "Prime numbers": {"terms": [2, 3, 5, 7, 11, 13, 17], "next": 19, "kind": "famous"},
    "Factorials": {"terms": [1, 2, 6, 24, 120], "next": 720, "kind": "famous"},
    "Mersenne numbers": {"terms": [1, 3, 7, 15, 31, 63], "next": 127, "kind": "famous"},
    "Catalan numbers": {"terms": [1, 1, 2, 5, 14, 42], "next": 132, "kind": "famous"},
}

ALL = list(SEQUENCES)

# kind -> [names], for the filter UI
KINDS: dict[str, list[str]] = {}
for _name, _data in SEQUENCES.items():
    KINDS.setdefault(_data["kind"], []).append(_name)


def slug(name: str) -> str:
    """Filename-safe slug for a sequence name (matches the rendered SVG)."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def prompt_text(name: str) -> str:
    """The terms shown on the card, ending in a blank to guess."""
    return ", ".join(str(t) for t in SEQUENCES[name]["terms"]) + ", ?"
