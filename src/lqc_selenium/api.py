#!/usr/bin/env python3

from datetime import datetime
import json
import os

from lqc.config.file_config import FileConfig


DEFAULT_RUN_SUMMARY_PATH = os.path.join(
    "bug_reports", "tester", "run_summary.json"
)
BUG_SNAPSHOT_INTERVAL = 10
RUNTIME_SECONDS_SNAPSHOT_INTERVAL = 1000

NUMERIC_SUMMARY_KEYS = {
    "tests_run",
    "passed",
    "bugs_found",
    "cant_reproduce",
    "bugs_with_no_modified_styles",
    "crashes",
    "bug_group_count",
    "single_bug_count",
    "grouped_bug_instance_count",
    "total_bug_directories",
    "runtime_seconds",
    "minify_seconds",
    "sorting_seconds",
    "true_minification_seconds",
}


def _default_summary(summary_path=DEFAULT_RUN_SUMMARY_PATH):
    target_root = os.path.abspath(os.path.dirname(summary_path))
    return {
        "updated_at": datetime.now().isoformat(),
        "target_root": target_root,
        "tests_run": 0,
        "passed": 0,
        "bugs_found": 0,
        "cant_reproduce": 0,
        "bugs_with_no_modified_styles": 0,
        "crashes": 0,
        "bug_group_count": 0,
        "single_bug_count": 0,
        "grouped_bug_instance_count": 0,
        "total_bug_directories": 0,
        "runtime_seconds": 0.0,
        "minify_seconds": 0.0,
        "sorting_seconds": 0.0,
        "true_minification_seconds": 0.0,
        "bug_groups": [],
        "single_bugs": [],
    }


def read_run_summary(summary_path=DEFAULT_RUN_SUMMARY_PATH):
    if not os.path.isfile(summary_path):
        return _default_summary(summary_path)

    try:
        with open(summary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return _default_summary(summary_path)

    summary = _default_summary(summary_path)
    summary.update(data if isinstance(data, dict) else {})
    return summary


def _write_summary_snapshot_once(payload, summary_path, snapshot_name):
    snapshot_path = os.path.join(os.path.dirname(summary_path), snapshot_name)
    if os.path.exists(snapshot_path):
        return

    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def _write_threshold_snapshots(payload, summary_path):
    bugs_found = int(payload.get("bugs_found", 0) or 0)
    max_bug_snapshot = (bugs_found // BUG_SNAPSHOT_INTERVAL) * BUG_SNAPSHOT_INTERVAL
    for bug_count in range(BUG_SNAPSHOT_INTERVAL, max_bug_snapshot + 1, BUG_SNAPSHOT_INTERVAL):
        _write_summary_snapshot_once(
            payload,
            summary_path,
            f"run_summary_{bug_count}_bugs.json",
        )

    runtime_seconds = float(payload.get("runtime_seconds", 0.0) or 0.0)
    max_runtime_snapshot = (
        int(runtime_seconds) // RUNTIME_SECONDS_SNAPSHOT_INTERVAL
    ) * RUNTIME_SECONDS_SNAPSHOT_INTERVAL
    for runtime_second in range(
        RUNTIME_SECONDS_SNAPSHOT_INTERVAL,
        max_runtime_snapshot + 1,
        RUNTIME_SECONDS_SNAPSHOT_INTERVAL,
    ):
        _write_summary_snapshot_once(
            payload,
            summary_path,
            f"run_summary_{runtime_second}s.json",
        )


def write_run_summary(summary, summary_path=DEFAULT_RUN_SUMMARY_PATH):
    payload = _default_summary(summary_path)
    payload.update(summary if isinstance(summary, dict) else {})
    payload["updated_at"] = datetime.now().isoformat()
    payload["target_root"] = os.path.abspath(os.path.dirname(summary_path))

    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    _write_threshold_snapshots(payload, summary_path)

    return summary_path


def get_sort_repo_dir():
    return FileConfig().bug_report_file_dir


def write_counter_run_summary(counter, target_root=None):
    if target_root is None:
        target_root = get_sort_repo_dir()

    os.makedirs(target_root, exist_ok=True)

    group_dirs = []
    single_bug_dirs = []
    grouped_bug_instances = 0

    for entry in os.listdir(target_root):
        entry_path = os.path.join(target_root, entry)
        if not os.path.isdir(entry_path):
            continue

        if entry.startswith("bug-group-"):
            group_dirs.append(entry)
            grouped_bug_instances += sum(
                1
                for child in os.listdir(entry_path)
                if os.path.isdir(os.path.join(entry_path, child)) and child.startswith("bug-")
            )
        elif entry.startswith("bug-"):
            single_bug_dirs.append(entry)

    summary = {
        "updated_at": datetime.now().isoformat(),
        "target_root": os.path.abspath(target_root),
        "tests_run": counter.num_tests,
        "passed": counter.num_successful,
        "bugs_found": counter.num_error,
        "cant_reproduce": counter.num_cant_reproduce,
        "bugs_with_no_modified_styles": counter.num_no_mod_styles_bugs,
        "crashes": counter.num_crash,
        "bug_group_count": len(group_dirs),
        "single_bug_count": len(single_bug_dirs),
        "grouped_bug_instance_count": grouped_bug_instances,
        "total_bug_directories": len(single_bug_dirs) + grouped_bug_instances,
        "bug_groups": sorted(group_dirs),
        "single_bugs": sorted(single_bug_dirs),
        "runtime_seconds": round(counter.getRuntimeSeconds(), 3),
        "minify_seconds": round(counter.total_minify_seconds, 3),
        "sorting_seconds": round(counter.total_sorting_seconds, 3),
        "true_minification_seconds": round(counter.total_true_minification_seconds, 3),
    }

    summary_path = os.path.join(target_root, "run_summary.json")
    write_run_summary(summary, summary_path=summary_path)
    return summary_path


def extract_bug_group_rules_to_json(
    source_root=None,
    output_json_path=None,
):
    if source_root is None:
        source_root = get_sort_repo_dir()
    if output_json_path is None:
        output_json_path = os.path.join(source_root, "rules.json")

    print(f"Extracting rules from {source_root} to {output_json_path}...")
    all_rules = []
    bug_group_folder_count = 0

    if not os.path.isdir(source_root):
        os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump({"rules": []}, f, indent=2)
        print("Found 0 bug-group folders.")
        return output_json_path, all_rules

    for root, _, files in os.walk(source_root):
        group_name = os.path.basename(root)
        if not group_name.startswith("bug-group-"):
            continue
        bug_group_folder_count += 1

        if "extracted_rule.json" not in files:
            continue

        extracted_rule_path = os.path.join(root, "extracted_rule.json")
        try:
            with open(extracted_rule_path, "r", encoding="utf-8") as f:
                rule = json.load(f)
        except OSError:
            continue
        except json.JSONDecodeError:
            continue

        all_rules.append(
            {
                "bug_group": os.path.relpath(root, source_root),
                "merged_tree_path": extracted_rule_path.replace("\\", "/"),
                "rule": rule,
            }
        )

    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump({"rules": all_rules}, f, indent=2)

    print(f"Found {bug_group_folder_count} bug-group folders.")
    return output_json_path, [entry["rule"] for entry in all_rules]


def item_add(item, amount=1, summary_path=DEFAULT_RUN_SUMMARY_PATH):
    summary = read_run_summary(summary_path)

    if item not in NUMERIC_SUMMARY_KEYS:
        raise ValueError(f"item_add only supports numeric summary keys. Got: {item}")

    current = summary.get(item, 0)
    if not isinstance(current, (int, float)):
        raise TypeError(f"Summary item '{item}' is not numeric.")
    if not isinstance(amount, (int, float)):
        raise TypeError("amount must be numeric.")

    summary[item] = current + amount
    write_run_summary(summary, summary_path)
    return summary[item]


def item_set(item, value, summary_path=DEFAULT_RUN_SUMMARY_PATH):
    summary = read_run_summary(summary_path)
    summary[item] = value
    write_run_summary(summary, summary_path)
    return value


def item_get(item, default=None, summary_path=DEFAULT_RUN_SUMMARY_PATH):
    summary = read_run_summary(summary_path)
    return summary.get(item, default)
