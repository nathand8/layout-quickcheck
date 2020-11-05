from functools import reduce


def generate_body_string(body, styles):
    def reduce_children(tree):
        return reduce(generate_element_string, tree, "")

    def generate_element_string(body_string, element):
        tag = element["tag"]
        style = ";".join([f"{name}:{value}" for name, value in styles.get(element["id"], {}).items()])
        element_id = element["id"]
        children_string = reduce_children(element["children"])
        current_template = """
          <{tag} style="{style}" id="{element_id}">
            {children_string}
          </{tag}>
        """
        return body_string + current_template.format(
            tag=tag,
            style=style,
            element_id=element_id,
            children_string=children_string,
        )

    return reduce_children(body)


def apply_log(body, styles):
    body_string = generate_body_string(body, styles)

    html_template = """
      <!DOCTYPE html>
      <html>
        <head>
          <title>Fuzzy layout</title>
        </head>
        <body style="scrollbar-width:none">
          {body_string}
        </body>
      </html>
    """

    return html_template.format(body_string=body_string)
