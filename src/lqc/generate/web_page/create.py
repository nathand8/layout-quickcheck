from enum import Enum, unique
from lqc.generate.web_page.util import formatWithIndent
from lqc.model.run_subject import RunSubject
from lqc.generate.web_page.html_body.create import create as html_body
from lqc.generate.web_page.javascript_with_debugging_tools.create import create as js_with_debug
from lqc.generate.web_page.javascript_minimal.create import create as js_minimal
from lqc.generate.web_page.javascript_grizzly.create import create as js_grizzly

html_template = """
<!DOCTYPE html>
<html>

  <head>
    <title>Layout QuickCheck</title>
    <!-- helpers.js and bootstrap.js can be used by testing frameworks (ie grizzly) -->
    <script src="helpers.js"></script>
    <script src="bootstrap.js"></script>
    <script>
      {js_string}
    </script>
  </head>

  <body>
    {body_string}
  </body>

</html>
"""

@unique
class JsVersion(Enum):
    DEBUGGING = 0
    MINIMAL = 1
    GRIZZLY = 2


def html_string(run_subject: RunSubject, js_version=JsVersion.DEBUGGING):

    body_string = html_body(run_subject)
    if js_version == JsVersion.DEBUGGING:
        js_string = js_with_debug(run_subject)
    elif js_version == JsVersion.MINIMAL:
        js_string = js_minimal(run_subject)
    elif js_version == JsVersion.GRIZZLY:
        js_string = js_grizzly(run_subject)

    return formatWithIndent(html_template, js_string=js_string, body_string=body_string)


def save_as_web_page(run_subject: RunSubject, file_path, use_minimal_js=False):
    with open(file_path, 'w') as file:
        file.write(html_string(run_subject, JsVersion.MINIMAL if use_minimal_js else JsVersion.DEBUGGING))

