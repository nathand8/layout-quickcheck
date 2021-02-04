import json
import os
import shutil
from test_config import TestConfig
from test_subject import TestSubject
from file_config import FileConfig
from web_page_creation.create import save_as_web_page


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
    test_config: TestConfig,
    test_subject: TestSubject,
    differences,
    original_filepath
):
    file_config = FileConfig()

    # Create a folder to hold all the bug report files
    bug_folder = os.path.join(file_config.bug_report_file_dir, f"bug-report-{test_config.timestamp}")
    os.mkdir(bug_folder)

    # Copy the original file
    bug_filepath = os.path.join(bug_folder, "bug.html")
    shutil.copy(original_filepath, bug_filepath)

    # Custom bug helper file
    bug_report_filename = f"bug-helper-{test_config.timestamp}.js"
    bug_helper_filepath = os.path.join(bug_folder, bug_report_filename)
    styles_used = list(set(all_style_names(test_subject.base_styles.map, test_subject.modified_styles.map)))
    styles_used.sort()
    styles_used_string = ",".join(styles_used)

    with open(bug_helper_filepath, "w") as f:
        f.write(f"const differences = {json.dumps(differences)}\n")
        f.write(f"const baseLog = {json.dumps(test_subject.base_styles.map)}\n")
        f.write(f"const styleLog = {json.dumps(test_subject.modified_styles.map)}\n")
        f.write(f"const stylesUsed = {json.dumps(styles_used)}\n")
        f.write(f'const stylesUsedString = "{styles_used_string}"\n')
    
    # Minimized file
    minimized_bug_filepath = os.path.join(bug_folder, "minimized_bug.html")
    save_as_web_page(test_subject, minimized_bug_filepath, True)