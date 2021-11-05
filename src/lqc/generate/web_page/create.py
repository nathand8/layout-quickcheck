from enum import Enum, unique
from lqc.generate.web_page.util import formatWithIndent
from lqc.model.run_result import RunResult
from lqc.model.run_subject import RunSubject
from lqc.generate.web_page.html_body.create import create as html_body
from lqc.generate.web_page.javascript_minimal.create import create as js_minimal

html_template = """<!DOCTYPE html>
<html>

  <head>
    <title>Layout QuickCheck</title>
    <script>
      {js_string}
    </script>
    <script src="debugging_tools.js"></script>
    {extra_js_files_string}
  </head>

  <body>
    {body_string}
  </body>

</html>
"""

def generate_extra_js_files_string(js_file_names):

    # <!-- helpers.js and bootstrap.js can be used by testing frameworks (ie grizzly) -->
    # <script src="helpers.js"></script>
    # <script src="bootstrap.js"></script>

    ret_string = ""
    for js_file_name in js_file_names:
        ret_string += f'<script src="{js_file_name}"></script>\n'
    return ret_string


def html_string(run_subject: RunSubject, run_result:RunResult=None, extra_js_file_names=[]):

    body_string = html_body(run_subject)
    extra_js_files_string = generate_extra_js_files_string(extra_js_file_names)
    js_string = js_minimal(run_subject, run_result)

    return formatWithIndent(html_template, js_string=js_string, body_string=body_string, extra_js_files_string=extra_js_files_string)


def save_as_web_page(run_subject: RunSubject, file_path, run_result=None):
    with open(file_path, 'w') as file:
        file.write(html_string(run_subject, run_result))

