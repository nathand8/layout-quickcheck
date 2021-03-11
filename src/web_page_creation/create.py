from run_subject import RunSubject
from web_page_creation.javascript_with_debugging_tools.create import create as js_with_debugging
from web_page_creation.javascript_minimal.create import create as js_minimal
from web_page_creation.html_body.create import create as html_body

html_template = """
<!DOCTYPE html>
<html>
  <head>
    <title>Fuzzy layout</title>
    <script>
    {js_string}
    </script>
  </head>
  <body>
    {body_string}
  </body>
</html>
"""

def html_string(run_subject: RunSubject, use_minimal_js=False):

    body_string = html_body(run_subject)
    if use_minimal_js:
        js_string = js_minimal(run_subject)
    else:
        js_string = js_with_debugging(run_subject)

    return html_template.format(body_string=body_string, js_string=js_string)


def save_as_web_page(run_subject: RunSubject, file_path, use_minimal_js=False):
    with open(file_path, 'w') as file:
        file.write(html_string(run_subject, use_minimal_js))

