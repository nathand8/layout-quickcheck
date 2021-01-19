import json
import os
import shutil


INCLUDE_VALUE_IN_NAME = ["display"]


def all_style_names(*style_dicts):
    for d in style_dicts:
        for _element_id, styles in d.items():
            for style_name, style_value in styles.items():
                if style_name in INCLUDE_VALUE_IN_NAME:
                    yield f"{style_name}:{style_value}"
                else:
                    yield style_name


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