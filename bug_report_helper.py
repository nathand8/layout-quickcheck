import json
import os
import shutil
from test_subject import TestSubject
from file_config import FileConfig
from web_page_creation.create import save_as_web_page
from datetime import datetime


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
    variants,
    test_subject: TestSubject,
    differences,
    original_filepath
):
    file_config = FileConfig()
    bug_folder = file_config.getTimestampBugReport()

    # Create a folder to hold all the bug report files
    os.mkdir(bug_folder)

    # Copy the original file
    bug_filepath = os.path.join(bug_folder, "original_bug.html")
    shutil.copy(original_filepath, bug_filepath)

    # Copy the minimized bug
    min_bug_with_debug = os.path.join(bug_folder, "min_bug_with_debug.html")
    save_as_web_page(test_subject, min_bug_with_debug)

    # Custom bug helper file - JSON file
    styles_used = list(set(all_style_names(test_subject.base_styles.map, test_subject.modified_styles.map)))
    styles_used.sort()
    styles_used_string = ",".join(styles_used)
    json_data = {
        "styles_used": styles_used,
        "styles_used_string": styles_used_string,
        "variants": variants,
        "differences": differences,
        "test_subject": test_subject,
    }

    json_data_filepath = os.path.join(bug_folder, "data.json")
    with open(json_data_filepath, "w") as f:
        f.write(json.dumps(json_data, indent=4, default=lambda o: o.__dict__))
    
    # Minimized file
    minimized_bug_filepath = os.path.join(bug_folder, "minimized_bug.html")
    save_as_web_page(test_subject, minimized_bug_filepath, True)
