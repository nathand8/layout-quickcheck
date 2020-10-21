import uuid
from random import random, choice
from css_generators.style_data import style_data
from css_generators.length import generate as generate_length
from css_generators.keyword import create_generator as create_keyword_generator

STYLE_PROBABILITY = 0.05
SUPPORTED_STYLE_TYPES = ["Length", "Keyword"]

has_children = {"body": 0.99, "div": 0.3}

has_multiple_children = {"body": 0.75, "div": 0.25}


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


def generate_style():
    styles = []
    for current_style in style_data["data"]:
        if random() <= STYLE_PROBABILITY:
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
                styles.append((style_name, style_value))
    return styles


# def generate_child(parent_tag):
#     child_tag = "div"
#     child_id = uuid.uuid4().hex
#     current_child = """
#           <{child_tag} style="{child_style}" id="{child_id}">
#             {grandchildren}
#           </{child_tag}>
#         """

#     grandchildren = generate_children(child_tag)
#     child_style = generate_style(child_tag)

#     return current_child.format(
#         child_style=child_style,
#         child_tag=child_tag,
#         grandchildren=grandchildren,
#         child_id=child_id,
#     )


def generate_child(parent_tag):
    child_tag = "div"
    child_id = uuid.uuid4().hex
    grandchildren = generate_children(child_tag)

    return {
        "tag": child_tag,
        "children": grandchildren,
        "id": child_id,
    }


def generate_children(parent_tag):
    children = []

    if random() <= has_children[parent_tag]:
        children.append(generate_child(parent_tag))
        while random() <= has_multiple_children[parent_tag]:
            children.append(generate_child(parent_tag))

    return children
