from random import random

style_probabilities = {
    'div': {
        'float': {
            'prob': 0.1,
            'values': {
                'left': 0.2,
                'right': 0.2,
                'none': 0.2,
                'inline-start': 0.2,
                'inline-end': 0.2
            }
        }
    }
}

has_children = {'body': 0.99, 'div': 0.6}

has_multiple_children = {'body': 0.75, 'div': 0.25}


def generate_style(tag):
    styles = []
    for style_name, style_properties in style_probabilities[tag].items():
        if random() <= style_properties['prob']:
            value_num = random()
            value_prob_sum = 0

            for value_name, value_prob in style_properties['values'].items():
                value_prob_sum += value_prob
                if value_num <= value_prob_sum:
                    styles.append((style_name, value_name))
                    break

    return ';'.join([f'{name}:{value}' for name, value in styles])


def generate_children(parent_tag):
    children = ''

    def generate_child(parent_tag):
        child_tag = 'div'
        current_child = """
          <{child_tag} style="{child_style}">
            {grandchildren}
          </{child_tag}>
        """

        grandchildren = generate_children(child_tag)
        child_style = generate_style(child_tag)

        return current_child.format(child_style=child_style,
                                    child_tag=child_tag,
                                    grandchildren=grandchildren)

    if random() <= has_children[parent_tag]:
        children += generate_child(parent_tag)

    while random() <= has_multiple_children[parent_tag]:
        children += generate_child(parent_tag)

    return children


def generate_layout():
    html = """
      <html>
        <head>
          <title>Fuzzy layout</title>
        </head>
        <body>
          {body}
        </body>
      </html>
    """

    body = generate_children('body')

    return html.format(body=body)
