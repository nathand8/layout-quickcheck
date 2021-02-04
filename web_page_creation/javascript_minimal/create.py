from test_subject import TestSubject

def create(test_subject: TestSubject):

    script_string = open('web_page_creation/javascript_minimal/template.js', 'r').read()
    return script_string.format(
        make_style_changes = make_style_changes(test_subject),
        get_dimensions = get_dimensions(test_subject)
    )

def make_style_changes(test_subject: TestSubject):
    """
    Create a string that will make style changes in javascript

    Example Output: 

        document.getElementById("912A37J38G").style["min-width"] = "200px";
        document.getElementById("912A37J38G").style["margin-left"] = "10em";
        document.getElementById("PTN873OUW").style["background-color"] = "blue";
        
    """
    ret_string = ""
    for (elementId, styles) in test_subject.modified_styles.map.items():
        for (style_name, style_value) in styles.items():
            ret_string += f'document.getElementById("{elementId}").style["{style_name}"] = "{style_value}";\n'
    
def get_dimensions(test_subject: TestSubject):
    """
    Create a string that will show dimensions for elements

    Example Output:

        console.log("#PTN873OUW", document.getElementById("PTN873OUW").getBoundingClientRect());

    """
    # TODO: Only show dimension changes for elements that actually change dimensions
    ret_string = ""
    for elementId in {**test_subject.base_styles.map, **test_subject.modified_styles.map}:
        ret_string += f'console.log("#{elementId}", document.getElementById("{elementId}").getBoundingClientRect());\n'
    
    return ret_string

