import uuid
import lorem
from random import random, choice
from css_generators.style_data import style_data
from css_generators.length import generate as generate_length
from css_generators.keyword import create_generator as create_keyword_generator
from css_generators.color import generate as generate_color

SUPPORTED_STYLE_TYPES = ["Length", "Keyword"]
STYLES_TO_IGNORE = ["content-visibility", "writing-mode"]

has_children = {"body": 0.99, "div": 0.3}
has_multiple_children = {"body": 0.75, "div": 0.25}
text_prob = 0.3
mult_sentence_prob = 0.2
newline_prob = 0.3


def type_to_generator(typedom_type, current_style):
    if typedom_type == "Length":
        return generate_length
    elif typedom_type == "Keyword":
        return create_keyword_generator(current_style["keywords"])


def is_supported_type(typedom_type, current_style):
    if typedom_type == "Length":
        return True
    elif typedom_type == "Keyword":
        return "keywords" in current_style
    else:
        return False


def generate_style(style_probability, is_base):
    styles = {"background-color": generate_color()} if is_base else {}
    for current_style in style_data["data"]:
        if current_style["name"] not in STYLES_TO_IGNORE:
            if random() <= style_probability:
                typedom_types = current_style.get("typedom_types", [])
                type_choices = [
                    choice
                    for choice in typedom_types
                    if is_supported_type(choice, current_style)
                ]
                if len(type_choices) > 0:
                    type_choice = choice(type_choices)
                    generator = type_to_generator(type_choice, current_style)
                    style_name = current_style["name"]
                    style_value = generator()
                    styles[style_name] = style_value
    return styles


def generate_child():
    child_tag = "div"
    child_id = uuid.uuid4().hex
    grandchildren = generate_children(child_tag)

    return {
        "tag": child_tag,
        "children": grandchildren,
        "id": child_id,
    }


def generate_text():
    text = lorem.sentence()
    while random() <= mult_sentence_prob:
        if random() <= newline_prob:
            text += "\n"
        text += " " + lorem.sentence()
    return {"tag": "<text>", "value": text, "children": []}


def generate_random_child_type():
    if random() <= text_prob:
        return generate_text()
    else:
        return generate_child()


def generate_children(parent_tag):
    children = []

    if random() <= has_children[parent_tag]:
        children.append(generate_random_child_type())
        while random() <= has_multiple_children[parent_tag]:
            children.append(generate_random_child_type())

    return children


def elements(tree):
    for element in tree:
        if element["tag"] != "<text>":
            yield element
            yield from elements(element["children"])


def generate_style_log(tree, style_probability, is_base):
    return {e["id"]: generate_style(style_probability, is_base) for e in elements(tree)}


def generate_layout_tree():
    return generate_children("body")
