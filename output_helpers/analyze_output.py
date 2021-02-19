import os
import sys
import json
import collections.abc

DEFAULT_BUG_REPORT_DIR = './bugreportfiles'
DEFAULT_JSON_FILENAME = 'data.json'

def collect_json_reports(bug_report_dir, json_filename):
    json_filepaths = [os.path.join(bug_report_dir, dir, json_filename) for dir in os.listdir(bug_report_dir)]
    reports = []
    for json_filepath in json_filepaths:
        with open(json_filepath, 'r') as f:
            reports.append(json.loads(f.read()))
    return reports

def get_matches(bugs, v_match):
    is_dict = lambda o: isinstance(o, collections.abc.Mapping)
    correct_format = lambda bug: is_dict(bug) and "variants" in bug and is_dict(bug["variants"]) and "Test Variant Summary" in bug["variants"] and is_dict(bug["variants"]["Test Variant Summary"])
    get_variants = lambda bug: bug["variants"]["Test Variant Summary"]
    return [bug for bug in bugs if correct_format(bug) and v_match(get_variants(bug))]

def count_matches(bugs, v_match):
    return len(get_matches(bugs, v_match))

if __name__ == "__main__":
    bug_report_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BUG_REPORT_DIR

    bugs = collect_json_reports(bug_report_dir, DEFAULT_JSON_FILENAME)

    print("Total Total:", len(bugs))
    print("Total:", count_matches(bugs, lambda v: True))
    print("Default:", count_matches(bugs, lambda v: v["Default Variant"]))
    print("Slow:", count_matches(bugs, lambda v: v["Slow - Forced Waits"]))
    print("Smaller Window:", count_matches(bugs, lambda v: v["Smaller Window Size"]))
    print("Larger Window:", count_matches(bugs, lambda v: v["Larger Window Size"]))
    print("JS Diff:", count_matches(bugs, lambda v: v["JavaScript Difference Detection"]))
    print("Firefox:", count_matches(bugs, lambda v: v["Firefox Browser"]))

    print("Unique StyleSets:", len(set([bug["styles_used_string"] for bug in bugs])))
    # print(json.dumps(bugs[-1], indent=4))
    
    # symmetric difference



