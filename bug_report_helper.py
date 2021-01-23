import json
import os
import shutil
from style_log_applier import generate_body_string
from test_subject import TestSubject


INCLUDE_VALUE_IN_NAME = ["display"]


def all_style_names(*style_dicts):
    for d in style_dicts:
        for _element_id, styles in d.items():
            for style_name, style_value in styles.items():
                if style_name in INCLUDE_VALUE_IN_NAME:
                    yield f"{style_name}:{style_value}"
                else:
                    yield style_name


def minimized_bug_report(test_subject):
    body_string = generate_body_string(test_subject.html_tree, test_subject.base_styles)

    make_style_changes = ""
    for (elementId, styles) in test_subject.modified_styles.items():
        for (style_name, style_value) in styles.items():
            make_style_changes += f'document.getElementById("{elementId}").style["{style_name}"] = "{style_value}";\n'
    
    # TODO: Only show dimension changes for elements that actually change dimensions
    get_dimensions = ""
    for elementId in {**test_subject.base_styles, **test_subject.modified_styles}:
        get_dimensions += f'console.log("#{elementId}", document.getElementById("{elementId}").getBoundingClientRect());\n'

    html_template = """
<!DOCTYPE html>
<html>
  <head>
    <title>Fuzzy layout</title>
    <script>
function simpleRecreate() {{

// Make the style changes
{make_style_changes}

// Get the dimensions
console.log("Dimensions after style changes, before reload");
{get_dimensions}

// Reload the elements
document.documentElement.innerHTML = document.documentElement.innerHTML;

// Get the dimensions again
console.log("Dimensions after reload");
{get_dimensions}

}}
    </script>
  </head>
  <body>
    {body_string}
        <div style="padding: 100px;">
            <button id="apply_styles_button">Apply Styles Above</button>
        </div>
  </body>
  <script>
    document.getElementById("apply_styles_button").onclick = simpleRecreate
  </script>
</html>
    """

    return html_template.format(
        body_string = body_string, 
        make_style_changes = make_style_changes, 
        get_dimensions = get_dimensions
    )


def save_bug_report(
    bug_report_parent_folder,
    test_file_path,
    formatted_timestamp,
    body,
    minified_base,
    minified_modified,
    postfix,
    differences,
    original_filepath
):
    # Create a folder to hold all the bug report files
    bug_folder = os.path.join(bug_report_parent_folder, f"bug-report-{formatted_timestamp}{postfix}")
    os.mkdir(bug_folder)

    # Copy the original file
    bug_filepath = os.path.join(bug_folder, "bug.html")
    shutil.copy(original_filepath, bug_filepath)

    # Custom bug helper file
    bug_report_filename = f"bug-helper-{formatted_timestamp}.js"
    bug_helper_filepath = os.path.join(bug_folder, bug_report_filename)
    styles_used = list(set(all_style_names(minified_base, minified_modified)))
    styles_used.sort()
    styles_used_string = ",".join(styles_used)

    with open(bug_helper_filepath, "w") as f:
        f.write(f"const differences = {json.dumps(differences)}\n")
        f.write(f"const baseLog = {json.dumps(minified_base)}\n")
        f.write(f"const styleLog = {json.dumps(minified_modified)}\n")
        f.write(f"const stylesUsed = {json.dumps(styles_used)}\n")
        f.write(f'const stylesUsedString = "{styles_used_string}"\n')
    
    # Minimized file
    minimized_bug_filepath = os.path.join(bug_folder, "minimized_bug.html")
    with open(minimized_bug_filepath, "w") as f:
        f.write(minimized_bug_report(TestSubject(body, minified_base, minified_modified)))
