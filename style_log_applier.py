from functools import reduce
import json


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
    style_string = json.dumps(styles)

    html_template = """
<!DOCTYPE html>
<html>
  <head>
    <title>Fuzzy layout</title>
    <!--
const styleLog = {style_string};

const outputDimensions = () => {{
  Array.from(document.getElementsByTagName('*')).forEach((element) => {{
    console.log(element.id, element.getBoundingClientRect());
  }});
}}

console.log('Dimensions before application');
outputDimensions();

Object.entries(styleLog).forEach(([id, styles]) => {{
  const element = document.getElementById(id);
  if (element) {{
    Object.entries(styles).forEach(([styleName, styleValue]) => {{
      element.style[styleName] = styleValue;
    }});
  }}
}});

console.log('Dimensions after application');
outputDimensions();

document.documentElement.innerHTML = document.documentElement.innerHTML;

console.log('Dimensions after fresh load');
outputDimensions();
    -->
  </head>
  <body>
    {body_string}
  </body>
</html>
    """

    return html_template.format(body_string=body_string, style_string=style_string)
