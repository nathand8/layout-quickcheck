
import os
from lqc.generate.web_page.util import indent
from lqc.model.run_subject import RunSubject


def create(run_subject: RunSubject):
    modified_style_string = run_subject.modified_styles.toJS()
    script_string = open(os.path.join(os.path.dirname(__file__), 'template.js'), 'r').read()
    driver_string = open(os.path.join(os.path.dirname(__file__), 'driver.js'), 'r').read()
    script_string = script_string.replace("__MODIFIED_STYLE_STRING__", indent("  ", modified_style_string))
    script_string = script_string.replace("__DRIVER_STRING__", driver_string)
    return script_string

