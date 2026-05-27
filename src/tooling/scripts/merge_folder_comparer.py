import argparse
import os
import sys

SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from lqc.rules.rule_engine import (
    create_rule,
    extract_tag_tree,
    check_all_pkls,
    get_base_styles,
    get_modified_styles,
    load_tree_start_pairs,
)
from lqc.rules.tree_merge import merge_trees

"""
Incrementally merges tree structures from PKL files in a merge folder,
generates a rule after each merge, and evaluates that rule against both
the merge folder and a separate check folder.

At each step two trees are merged, a rule is constructed from the merged
tree, and that rule is tested against all PKL files in both folders to
measure how well it matches the merge dataset and whether it incorrectly
matches items in the check dataset.

Usage
-----
python src/tooling/scripts/merge_folder_comparer.py --merge <merge_folder_path> --check <check_folder_path>

Arguments
---------
--merge
    Path to the folder containing PKL files used to build and merge trees.

--check
    Path to the folder containing PKL files used to test whether generated
    rules incorrectly match unrelated data.


Output
------
For each merge step the script prints the generated tree, the rule derived
from that tree, and the number of matches in both the merge and check
folders reported as (true_count, false_count).
"""


def run_graph_pipeline(merge_folder, check_folder):
    treeLists=[]
    ruleLists=[]
    baseLists=[]
    checkLists=[]

    pairs = load_tree_start_pairs(merge_folder)
    _, cur_start = pairs.pop(0)

    for _, start_node in pairs:
        cur_tree, cur_start = merge_trees(cur_start, start_node)

        treeLists.append(cur_tree)

        rule = create_rule(
            extract_tag_tree(cur_tree),
            get_base_styles(cur_start),
            get_modified_styles(cur_start),
        )
        ruleLists.append(rule)

        results, true_count, false_count = check_all_pkls(check_folder, [rule])
        checkLists.append((true_count, false_count))
        results, true_count, false_count = check_all_pkls(merge_folder, [rule])
        baseLists.append((true_count, false_count))

    return treeLists, ruleLists, baseLists, checkLists





if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--merge", required=True, help="Path to merge folder")
    parser.add_argument("--check", required=True, help="Path to check folder")

    args = parser.parse_args()

    results = run_graph_pipeline(
        args.merge,
        args.check
    )

    for item in results:
        print("==== New Result ====")
        print(item)

