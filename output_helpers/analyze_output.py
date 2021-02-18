import os
import sys
import json

DEFAULT_BUG_REPORT_DIR = './bugreportfiles'
DEFAULT_JSON_FILENAME = 'data.json'

def collect_json_reports(bug_report_dir, json_filename):
    json_filepaths = [os.path.join(bug_report_dir, dir, json_filename) for dir in os.listdir(bug_report_dir)]
    reports = []
    for json_filepath in json_filepaths:
        with open(json_filepath, 'r') as f:
            reports.append(json.loads(f.read()))
    
    return reports


if __name__ == "__main__":
    bug_report_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_BUG_REPORT_DIR

    reports = collect_json_reports(bug_report_dir, DEFAULT_JSON_FILENAME)
    print(json.dumps(reports[0], indent=4))



