import json
import os
import shutil
from datetime import datetime
from lqc.config.file_config import FileConfig
from lqc.generate.web_page.create import save_as_web_page

from lqc.model.run_subject import RunSubject
from lqc.selenium_harness.layout_tester import PAGE_CRASH


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
    run_subject: RunSubject,
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
    save_as_web_page(run_subject, min_bug_with_debug)

    # Custom bug helper file - JSON file
    styles_used = list(set(all_style_names(run_subject.base_styles.map, run_subject.modified_styles.map)))
    styles_used.sort()
    styles_used_string = ",".join(styles_used)
    base_styles = list(set(all_style_names(run_subject.base_styles.map)))
    modified_styles = list(set(all_style_names(run_subject.modified_styles.map)))
    bug_type = "Page Crash" if differences == PAGE_CRASH else "Under Invalidation"
    json_data = {
        "datetime": datetime.now().isoformat(),
        "bug_type": bug_type,
        "styles_used": styles_used,
        "styles_used_string": styles_used_string,
        "base_styles": base_styles,
        "modified_styles": modified_styles,
        "variants": variants,
        "differences": differences,
        "run_subject": run_subject,
    }

    json_data_filepath = os.path.join(bug_folder, "data.json")
    with open(json_data_filepath, "w") as f:
        f.write(json.dumps(json_data, indent=4, default=lambda o: o.__dict__))
    
    # Minimized file
    minimized_bug_filepath = os.path.join(bug_folder, "minimized_bug.html")
    save_as_web_page(run_subject, minimized_bug_filepath, True)

    # Return a URL
    url = "file://" + os.path.abspath(min_bug_with_debug)
    return url
