import os
import sys
import json
import collections.abc

DEFAULT_JSON_FILENAME = 'data.json'

def collect_json_reports(bug_report_dir, json_filename):
    json_filepaths = [os.path.join(bug_report_dir, dir, json_filename) for dir in os.listdir(bug_report_dir)]
    reports = {}
    for json_filepath in json_filepaths:
        if os.path.exists(json_filepath):
            with open(json_filepath, 'r') as f:
                reports[json_filepath] = json.loads(f.read())
    return reports

def get_matching_paths(reports):
    matching_paths = []
    for (path, report_json) in reports.items():
        if "variants" in report_json:
            variants = report_json["variants"]
            if "Test Variant Summary" in variants:
                summary = variants["Test Variant Summary"]
                if "Firefox:layout.css.grid-item-baxis-measurement.enabled=true" in summary:
                    foundWhenEnabled = summary["Firefox:layout.css.grid-item-baxis-measurement.enabled=true"]
                    if "Firefox:layout.css.grid-item-baxis-measurement.enabled=false" in summary:
                        foundWhenDisabled = summary["Firefox:layout.css.grid-item-baxis-measurement.enabled=false"]
                        if foundWhenEnabled and not foundWhenDisabled:
                            matching_paths.append("")
                            if "styles_used_string" in report_json:
                                matching_paths.append(report_json["styles_used_string"])
                            matching_paths.append(path)
                            matching_paths.append("")

    return matching_paths


if __name__ == "__main__":
    bug_report_dir = sys.argv[1]
    reports = collect_json_reports(bug_report_dir, DEFAULT_JSON_FILENAME)
    matching_paths = get_matching_paths(reports)
    for path in matching_paths:
        print(path)





