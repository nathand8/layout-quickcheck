from functools import reduce
import json
from test_subject import TestSubject


def create(test_subject: TestSubject):

    body = test_subject.html_tree
    styles = test_subject.base_styles

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
