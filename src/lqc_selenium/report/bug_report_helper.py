import json
import os
import shutil
from datetime import datetime
from lqc.config.file_config import FileConfig
from lqc.generate.web_page.create import save_as_web_page
from lqc.generate.web_page.run_subject_converter import copyExternalJSFiles
from lqc.model.constants import BugType
from lqc.model.run_result import RunResult, RunResultLayoutBug
from lqc.model.run_subject import RunSubject


def save_bug_report(
    variants,
    run_subject: RunSubject,
    run_result: RunResult,
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
    minified_bug = os.path.join(bug_folder, "minified_bug.html")
    save_as_web_page(run_subject, minified_bug, run_result=run_result)
    copyExternalJSFiles(bug_folder)

    # Custom bug helper file - JSON file
    styles_used = list(run_subject.all_style_names())
    styles_used.sort()
    styles_used_string = ",".join(styles_used)
    base_styles = list(run_subject.base_styles.all_style_names())
    modified_styles = list(run_subject.modified_styles.all_style_names())
    bug_type = "Page Crash" if run_result.type == BugType.PAGE_CRASH else "Under Invalidation"
    json_data = {
        "datetime": datetime.now().isoformat(),
        "bug_type": bug_type,
        "styles_used": styles_used,
        "styles_used_string": styles_used_string,
        "base_styles": base_styles,
        "styles_signature": run_subject.styles_signature(),
        "modified_styles": modified_styles,
        "variants": variants,
        "run_subject": run_subject,
    }
    if isinstance(run_result, RunResultLayoutBug):
        json_data["differences"] = run_result.element_dimensions

    json_data_filepath = os.path.join(bug_folder, "data.json")
    with open(json_data_filepath, "w") as f:
        f.write(json.dumps(json_data, indent=4, default=lambda o: o.__dict__))

    # Todo: Copy the necessary javascript files (debugger_tools.js)

    # Return a URL
    url = "file://" + os.path.abspath(minified_bug)
    return url
