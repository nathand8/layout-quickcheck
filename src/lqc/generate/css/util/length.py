from random import choice
import re
from lqc.generate.css.util.number import generate as generate_number

suffixes = [
    "cap",
    "ch",
    "em",
    "ex",
    "ic",
    "lh",
    "rem",
    "rlh",
    "vh",
    "vw",
    "vi",
    "vb",
    "vmin",
    "vmax",
    "px",
    "cm",
    "mm",
    "Q",
    "in",
    "pc",
    "pt",
    "mozmm",
    "",
]


def generate_suffix():
    return choice(suffixes)


def generate():
    number = generate_number()
    suffix = generate_suffix()
    return f"{number}{suffix}"


def matches_length_pattern(style_string):
    LENGTH_RE = r'^([+-]*)([0-9]+)([a-zA-Z]+)$' # Matches numbers followed by letters e.g "100px", "2000"
    match = re.match(LENGTH_RE, style_string)
    if match is None:
        return False
    number_prefix, number, suffix = match.groups()
    return suffix in suffixes

    
