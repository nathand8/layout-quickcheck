from random import random

has_children = {'body': 0.99, 'div': 0.6}

has_multiple_children = {'body': 0.75, 'div': 0.25}


def generate_children(parent_tag):
    children = ''

    def generate_child(parent_tag):
        child_tag = 'div'
        current_child = """
        <{child_tag}>
          {grandchildren}
        </{child_tag}>
      """

        grandchildren = generate_children(child_tag)

        return current_child.format(child_tag=child_tag,
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
