import argparse
import os
import sys

SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from lqc.config.config import Config, parse_config
from lqc_selenium.api import extract_bug_group_rules_to_json


DEFAULT_CONFIG_FILE = "./config/change.json"
DEFAULT_SOURCE_ROOT = "bug_reports/tester"
DEFAULT_OUTPUT_JSON = "bug_reports/tester/rules.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=DEFAULT_CONFIG_FILE, help="Path to config JSON")
    parser.add_argument("--source-root", default=DEFAULT_SOURCE_ROOT, help="Folder to scan for merged_tree.txt files")
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON, help="Path to write extracted rules JSON")
    args = parser.parse_args()

    conf = parse_config(args.config)
    Config(conf)

    current_rules = Config().getRules()
    print(current_rules, "\n")

    _, rules = extract_bug_group_rules_to_json(
        source_root=args.source_root,
        output_json_path=args.output_json,
    )

    if not rules:
        rules = current_rules

    print(rules, "\n")


if __name__ == "__main__":
    main()
