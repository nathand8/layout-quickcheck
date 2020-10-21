from style_log_generator import generate_style, generate_children
from style_log_applier import apply_log


def elements(tree):
    for element in tree:
        yield element
        yield from elements(element["children"])


def generate_layout():
    body = generate_children("body")
    style_log = {e["id"]: generate_style() for e in elements(body)}

    return apply_log(body, style_log)
