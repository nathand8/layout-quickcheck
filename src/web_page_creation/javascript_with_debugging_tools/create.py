import json
from run_subject import RunSubject

def create(run_subject: RunSubject):
    modified_style_string = run_subject.modified_styles.toJS()
    script_string = open('src/web_page_creation/javascript_with_debugging_tools/template.js', 'r').read()
    return script_string.replace("__MODIFIED_STYLE_STRING__", modified_style_string)
