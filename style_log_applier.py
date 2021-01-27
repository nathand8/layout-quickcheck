from functools import reduce
import json


def generate_body_string(body, styles):
    def reduce_children(tree):
        return reduce(generate_element_string, tree, "")

    def generate_element_string(body_string, element):
        tag = element["tag"]
        if tag == "<text>":
            return body_string + element["value"]
        else:
            style = ";".join(
                [
                    f"{name}:{value}"
                    for name, value in styles.get(element["id"], {}).items()
                ]
            )
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


def apply_log(body, styles, modified_styles):
    body_string = generate_body_string(body, styles)
    modified_style_string = json.dumps(modified_styles)
    recreate_problem_js_string = open('recreate_template.js', 'r').read().replace("__MODIFIED_STYLE_STRING__", modified_style_string)

    html_template = """
<!DOCTYPE html>
<html>
  <head>
    <script type="text/javascript" src="/jsdist/main.js"></script>
    <title>Fuzzy layout</title>
    <script>
    {recreate_problem_js_string}
    </script>
  </head>
  <body>
    {body_string}
  </body>
</html>
    """

    return html_template.format(
        body_string=body_string, recreate_problem_js_string=recreate_problem_js_string
    )
