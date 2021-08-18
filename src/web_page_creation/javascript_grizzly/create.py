from lqc.run_subject import RunSubject
from lqc.web_page_creation.util import indent

def create(run_subject: RunSubject):
    modified_style_string = run_subject.modified_styles.toJS()
    script_string = open('src/web_page_creation/javascript_grizzly/template.js', 'r').read()
    return script_string.replace("__MODIFIED_STYLE_STRING__", indent("  ", modified_style_string))