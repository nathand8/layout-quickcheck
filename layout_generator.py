from random import random, randint, choice
from css_generators.style_data import style_data
from css_generators.length import generate as generate_length
from css_generators.keyword import create_generator as create_keyword_generator
import uuid


STYLE_PROBABILITY = 0.05
SUPPORTED_STYLE_TYPES = ['Length', 'Keyword']


def generate_color():
    red = randint(0, 255)
    blue = randint(0, 255)
    green = randint(0, 255)
    return f'#{red:02x}{blue:02x}{green:02x}'


def type_to_generator(typedom_type, current_style):
    if typedom_type == 'Length':
        return generate_length
    elif typedom_type == 'Keyword':
        return create_keyword_generator(current_style['keywords'])


def is_supported_type(typedom_type, current_style):
    if typedom_type == 'Length':
        return True
    elif typedom_type == 'Keyword':
        return 'keywords' in current_style
    else:
        return False


has_children = {'body': 0.99, 'div': 0.3}

has_multiple_children = {'body': 0.75, 'div': 0.25}


def generate_style(tag):
    styles = []
    for current_style in style_data['data']:
        if random() <= STYLE_PROBABILITY:
            typedom_types = current_style.get('typedom_types', [])
            type_choices = [choice for choice in typedom_types
                            if is_supported_type(choice, current_style)]
            if len(type_choices) > 0:
                type_choice = choice(type_choices)
                generator = type_to_generator(type_choice, current_style)
                style_name = current_style['name']
                style_value = generator()
                styles.append((style_name, style_value))
    return ';'.join([f'{name}:{value}' for name, value in styles])


def generate_children(parent_tag):
    children = ''

    def generate_child(parent_tag):
        child_tag = 'div'
        child_id = uuid.uuid4().hex
        current_child = """
          <{child_tag} style="{child_style}" id="{child_id}">
            {grandchildren}
          </{child_tag}>
        """

        grandchildren = generate_children(child_tag)
        child_style = generate_style(child_tag)

        return current_child.format(child_style=child_style,
                                    child_tag=child_tag,
                                    grandchildren=grandchildren,
                                    child_id=child_id)

    if random() <= has_children[parent_tag]:
        children += generate_child(parent_tag)

    while random() <= has_multiple_children[parent_tag]:
        children += generate_child(parent_tag)

    return children


def generate_layout():
    html = """
      <!DOCTYPE html>
      <html>
        <head>
          <title>Fuzzy layout</title>
        </head>
        <body style="scrollbar-width:none">
          {body}
        </body>
      </html>
    """

    body = generate_children('body')

    return html.format(body=body)
