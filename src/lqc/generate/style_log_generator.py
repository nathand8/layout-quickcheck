import uuid
import lorem
from random import random, choice
from lqc.config.config import Config
from lqc.generate.css.style_data import style_data
from lqc.generate.css.style_generator import StyleGenerator
from lqc.generate.css.util import length, keyword
from lqc.model.run_subject import RunSubject
from lqc.model.element_tree import ElementTree
from lqc.model.style_map import StyleMap

SUPPORTED_STYLE_TYPES = ["Length", "Keyword"]

has_children = {"body": 0.99, "div": 0.3}
has_multiple_children = {"body": 0.75, "div": 0.25}
text_prob = 0.3
mult_sentence_prob = 0.2
newline_prob = 0.3


def type_to_generator(typedom_type, current_style):
    if typedom_type == "Length":
        return length.generate()
    elif typedom_type == "Keyword":
        return keyword.create_generator(current_style["keywords"])


def is_supported_type(typedom_type, current_style):
    if typedom_type == "Length":
        return True
    elif typedom_type == "Keyword":
        return "keywords" in current_style
    else:
        return False


def generate_styles():
    styles = {}
    style_config = Config()
    style_value_generator = StyleGenerator()
    for current_style in style_data["data"]:
        style_probability = style_config.getStyleProbability(current_style["name"])
        if random() < style_probability:
            gen = style_value_generator.pickGenerator(current_style)
            if gen:
                style_name = current_style["name"]
                style_value = gen()
                styles[style_name] = style_value
    return styles


def generate_child():
    child_tag = "div"
    child_id = uuid.uuid4().hex
    for n in range(10): # Replace the numbers with letters, for ease of use in JS
        child_id = child_id.replace(str(n), choice("abcdefghijklmnopqrstuvwxyz"))

    grandchildren = generate_children(child_tag)

    return {
        "tag": child_tag,
        "children": grandchildren,
        "id": child_id,
    }


def generate_text():
    text = lorem.sentence()
    while random() < mult_sentence_prob:
        if random() < newline_prob:
            text += "\n"
        text += " " + lorem.sentence()
    return {"tag": "<text>", "value": text, "children": []}


def generate_random_child_type():
    if random() < text_prob:
        return generate_text()
    else:
        return generate_child()


def generate_children(parent_tag):
    children = []

    if random() < has_children[parent_tag]:
        children.append(generate_random_child_type())
        while random() <= has_multiple_children[parent_tag]:
            children.append(generate_random_child_type())

    return children


def elements(tree):
    for element in tree:
        if element["tag"] != "<text>":
            yield element
            yield from elements(element["children"])


def generate_style_log(tree):
    return {e["id"]: generate_styles() for e in elements(tree)}


def generate_layout_tree():
    return generate_children("body")


def generate_run_subject():
    body = generate_layout_tree()
    base_style_log = generate_style_log(body)
    modified_style_log = generate_style_log(body)

    return RunSubject(ElementTree(body), StyleMap(base_style_log), StyleMap(modified_style_log))
