import os,json
from lqc.generate.web_page.util import formatWithIndent
from lqc.model.run_result import RunResult, RunResultLayoutBug
from lqc.model.run_subject import RunSubject

EXTERNAL_JS_FILE_PATHS = [
    os.path.join(os.path.dirname(__file__), 'debugging_tools.js')
]


def create(run_subject: RunSubject, run_result: RunResult):

    script_string = open(os.path.join(os.path.dirname(__file__), 'minimal.js'), 'r').read()
    return formatWithIndent(script_string,
        make_style_changes = make_style_changes(run_subject),
        get_dimensions = get_dimensions(run_subject, run_result)
    )


def make_style_changes(run_subject: RunSubject):
    return run_subject.modified_styles.toJS()

    
def get_dimensions(run_subject: RunSubject, run_result: RunResult):
    """
    Create a string that will show dimensions for elements

    Example Output:

        console.log("#PTN873OUW", document.getElementById("PTN873OUW").getBoundingClientRect());

    """
    ret_string = ""
    if run_result and isinstance(run_result, RunResultLayoutBug):
        for el in run_result.element_dimensions:
            if el['id']:
                elementId = json.dumps(el['id'])
                differing_dims = json.dumps(el["differing_dims"])
                ret_string += f'console.log("#" + {elementId}, filterDimensions(document.getElementById({elementId}).getBoundingClientRect(), {differing_dims}));\n'
    
    else:
        for elementId in run_subject.getElementIds():
            ret_string += f'console.log("#{elementId}", document.getElementById("{elementId}").getBoundingClientRect());\n'
    
    return ret_string

