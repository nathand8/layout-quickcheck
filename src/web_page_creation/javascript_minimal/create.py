from lqc.run_subject import RunSubject
from lqc.web_page_creation.util import formatWithIndent

def create(run_subject: RunSubject):

    script_string = open('src/web_page_creation/javascript_minimal/template.js', 'r').read()
    return formatWithIndent(script_string,
        make_style_changes = make_style_changes(run_subject),
        get_dimensions = get_dimensions(run_subject)
    )


def make_style_changes(run_subject: RunSubject):
    return run_subject.modified_styles.toJS()

    
def get_dimensions(run_subject: RunSubject):
    """
    Create a string that will show dimensions for elements

    Example Output:

        console.log("#PTN873OUW", document.getElementById("PTN873OUW").getBoundingClientRect());

    """
    # TODO: Only show dimension changes for elements that actually change dimensions
    ret_string = ""
    for elementId in run_subject.getElementIds():
        ret_string += f'console.log("#{elementId}", document.getElementById("{elementId}").getBoundingClientRect());\n'
    
    return ret_string

