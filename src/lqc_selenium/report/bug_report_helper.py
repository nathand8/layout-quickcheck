import json
import os
import shutil
import pickle
from datetime import datetime
from lqc.config.file_config import FileConfig
from lqc.generate.web_page.create import save_as_web_page
from lqc.generate.web_page.run_subject_converter import copyExternalJSFiles
from lqc.model.constants import BugType
from lqc.model.run_result import RunResult, RunResultLayoutBug
from lqc.model.run_subject import RunSubject
from lqc.rules.rule_engine import dissolve_bug_group, recompute_bug_group_artifacts


def save_bug_report(
    variants,
    minified_run_subject: RunSubject,
    run_result: RunResult,
    original_filepath,
    prerun_subject: RunSubject,
    shouldSkip,
    path=None,
    rule_name=None,
    sorting_seconds=None,
    true_minification_seconds=None,
):
    # If there is no minified subject due rule matching then set it to the prerun subject.
    if minified_run_subject is None:
        minified_run_subject = prerun_subject

    # no group path, create a new bug folder in the default location
    if path is None:
        raise ValueError("Path must be provided to save bug report")
    else:
        #create a new bug folder inside the provided path if the path is a bug group, otherwise use the provided path as the bug folder
        group_path = (
            path
            if os.path.basename(os.path.normpath(path)).startswith("bug-group-")
            else None
        )

        if group_path is not None:
            bug_folder = os.path.join(
                path,
                f"bug-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            )
        else:
            raise ValueError(f"Provided path {path} is not a valid bug group path")

    matched_rule_folder = group_path

    print(f"[save_bug_report] creating bug_folder: {os.path.abspath(bug_folder)}")

    os.makedirs(bug_folder, exist_ok=True)

    # Copy the original file
    bug_filepath = os.path.join(bug_folder, "original_bug.html")
    shutil.copy(original_filepath, bug_filepath)

    # Copy the minimized bug
    minified_bug = os.path.join(bug_folder, "minified_bug.html")
    print(f"Saving minimized bug to {minified_bug}")
    save_as_web_page(minified_run_subject, minified_bug, run_result=run_result)
    copyExternalJSFiles(bug_folder)

    # Custom bug helper file - JSON file
    styles_used = list(minified_run_subject.all_style_names())
    styles_used.sort()
    styles_used_string = ",".join(styles_used)
    base_styles = list(minified_run_subject.base_styles.all_style_names())
    modified_styles = list(minified_run_subject.modified_styles.all_style_names())
    bug_type = "Page Crash" if run_result.type == BugType.PAGE_CRASH else "Under Invalidation"

    pickle_addr = os.path.join(bug_folder, "minified_run_subject.pkl")
    with open(pickle_addr, "wb") as f:
        pickle.dump(minified_run_subject, f)

    prerun_subject_addr = os.path.join(bug_folder, "run_subject_prerun.pkl")
    with open(prerun_subject_addr, "wb") as f:
        pickle.dump(prerun_subject, f)

    json_data = {
        "datetime": datetime.now().isoformat(),
        "bug_type": bug_type,
        "styles_used": styles_used,
        "styles_used_string": styles_used_string,
        "base_styles": base_styles,
        "modified_styles": modified_styles,
        "variants": variants,
        "minified_run_subject": minified_run_subject,
        "prerun_subject": prerun_subject,
        "pickle_addr": pickle_addr,
        "shouldSkip": shouldSkip,
        "matched_rule_name": rule_name,
        "matched_rule_folder": matched_rule_folder,
        "sorting_seconds": sorting_seconds,
        "true_minification_seconds": true_minification_seconds,
    }
    
    if isinstance(run_result, RunResultLayoutBug):
        json_data["differences"] = run_result.element_dimensions

    json_data_filepath = os.path.join(bug_folder, "data.json")
    with open(json_data_filepath, "w") as f:
        f.write(json.dumps(json_data, indent=4, default=lambda o: o.__dict__))

    if group_path is not None:
        rule = recompute_bug_group_artifacts(group_path)
        if rule is None:
            raise ValueError(f"Could not find rule for bug group at {group_path}")
            moved_paths = dissolve_bug_group(group_path)
            moved_bug_folder = moved_paths.get(os.path.abspath(bug_folder))
            if moved_bug_folder is not None:
                minified_bug = os.path.join(moved_bug_folder, "minified_bug.html")

    url = "file://" + os.path.abspath(minified_bug)
    return url
