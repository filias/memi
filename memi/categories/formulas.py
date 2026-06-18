"""Formulas for the Science category.

Each formula maps a name (the answer — what the formula is *for*) to its
LaTeX (rendered to an SVG shown on the card) and a field (used as the
pre-reveal clue and the filter). Keep the LaTeX within matplotlib's
mathtext subset — it's what scripts/render_formulas.py uses to draw them.
"""

import re

FORMULAS = {
    # Geometry
    "Area of a circle": {"latex": r"A = \pi r^2", "field": "geometry"},
    "Circumference of a circle": {"latex": r"C = 2 \pi r", "field": "geometry"},
    "Area of a triangle": {"latex": r"A = \frac{1}{2} b h", "field": "geometry"},
    "Area of a trapezoid": {"latex": r"A = \frac{a + b}{2} h", "field": "geometry"},
    "Pythagorean theorem": {"latex": r"a^2 + b^2 = c^2", "field": "geometry"},
    "Volume of a cylinder": {"latex": r"V = \pi r^2 h", "field": "geometry"},
    "Volume of a sphere": {"latex": r"V = \frac{4}{3} \pi r^3", "field": "geometry"},
    "Surface area of a sphere": {"latex": r"A = 4 \pi r^2", "field": "geometry"},
    "Volume of a cone": {"latex": r"V = \frac{1}{3} \pi r^2 h", "field": "geometry"},
    "Volume of a cube": {"latex": r"V = a^3", "field": "geometry"},
    # Algebra
    "Quadratic formula": {"latex": r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}", "field": "algebra"},
    "Slope of a line": {"latex": r"m = \frac{y_2 - y_1}{x_2 - x_1}", "field": "algebra"},
    "Distance between two points": {"latex": r"d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}", "field": "algebra"},
    "Difference of squares": {"latex": r"a^2 - b^2 = (a + b)(a - b)", "field": "algebra"},
    "Square of a binomial": {"latex": r"(a + b)^2 = a^2 + 2ab + b^2", "field": "algebra"},
    "Compound interest": {"latex": r"A = P \left(1 + \frac{r}{n}\right)^{nt}", "field": "algebra"},
    "Sum of an arithmetic series": {"latex": r"S_n = \frac{n}{2}(a_1 + a_n)", "field": "algebra"},
    # Trigonometry
    "Pythagorean identity": {"latex": r"\sin^2\theta + \cos^2\theta = 1", "field": "trigonometry"},
    "Law of cosines": {"latex": r"c^2 = a^2 + b^2 - 2ab\cos C", "field": "trigonometry"},
    "Law of sines": {"latex": r"\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C}", "field": "trigonometry"},
    "Definition of tangent": {"latex": r"\tan\theta = \frac{\sin\theta}{\cos\theta}", "field": "trigonometry"},
    "Sine double angle": {"latex": r"\sin 2\theta = 2\sin\theta\cos\theta", "field": "trigonometry"},
    # Physics
    "Newton's second law": {"latex": r"F = ma", "field": "physics"},
    "Mass–energy equivalence": {"latex": r"E = mc^2", "field": "physics"},
    "Kinetic energy": {"latex": r"E_k = \frac{1}{2} m v^2", "field": "physics"},
    "Gravitational potential energy": {"latex": r"E_p = mgh", "field": "physics"},
    "Newton's law of gravitation": {"latex": r"F = G \frac{m_1 m_2}{r^2}", "field": "physics"},
    "Ohm's law": {"latex": r"V = IR", "field": "physics"},
    "Work done": {"latex": r"W = Fd", "field": "physics"},
    "Power": {"latex": r"P = \frac{W}{t}", "field": "physics"},
    "Density": {"latex": r"\rho = \frac{m}{V}", "field": "physics"},
    "Momentum": {"latex": r"p = mv", "field": "physics"},
    "Wave speed": {"latex": r"v = f \lambda", "field": "physics"},
    "Hooke's law": {"latex": r"F = -kx", "field": "physics"},
    "Coulomb's law": {"latex": r"F = k \frac{q_1 q_2}{r^2}", "field": "physics"},
    "Energy of a photon": {"latex": r"E = h f", "field": "physics"},
    # Chemistry
    "Ideal gas law": {"latex": r"PV = nRT", "field": "chemistry"},
    "Molarity": {"latex": r"c = \frac{n}{V}", "field": "chemistry"},
    "Number of moles": {"latex": r"n = \frac{m}{M}", "field": "chemistry"},
    "pH": {"latex": r"pH = -\log[H^+]", "field": "chemistry"},
    "Gibbs free energy": {"latex": r"\Delta G = \Delta H - T \Delta S", "field": "chemistry"},
    # Calculus
    "Power rule (derivative)": {"latex": r"\frac{d}{dx} x^n = n x^{n-1}", "field": "calculus"},
    "Definition of the derivative": {"latex": r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}", "field": "calculus"},
    "Power rule (integral)": {"latex": r"\int x^n \, dx = \frac{x^{n+1}}{n+1} + C", "field": "calculus"},
    # Statistics
    "Arithmetic mean": {"latex": r"\bar{x} = \frac{1}{n} \sum x_i", "field": "statistics"},
    "Standard deviation": {"latex": r"\sigma = \sqrt{\frac{1}{n} \sum (x_i - \bar{x})^2}", "field": "statistics"},
}

ALL = list(FORMULAS)

# field -> [names], for the filter UI and the science:all aggregate
FIELDS: dict[str, list[str]] = {}
for _name, _data in FORMULAS.items():
    FIELDS.setdefault(_data["field"], []).append(_name)


def slug(name: str) -> str:
    """Filename-safe slug for a formula name (matches the rendered SVG)."""
    s = name.lower().replace("–", "-").replace("—", "-").replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")
