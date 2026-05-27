#!/usr/bin/env python3

import argparse
import os
import pickle
import sys
from time import time
import traceback
from lqc.config.config import Config, parse_config
from lqc.generate.html_file_generator import remove_file
from lqc.generate.style_log_generator import generate_run_subject
from lqc.minify.minify_test_file import MinifyStepFactory
from lqc.model.constants import BugType
from lqc.util.counter import Counter
from lqc_selenium.report.bug_report_helper import save_bug_report
from lqc_selenium.selenium_harness.layout_tester import test_combination
from lqc_selenium.variants.variant_tester import test_variants
from lqc_selenium.variants.variants import TargetBrowser, getTargetVariant
from lqc_selenium.api import get_sort_repo_dir, write_counter_run_summary as write_run_summary
from lqc.rules.rule_engine import sort_single_bug


def minify(target_browser, run_subject):
    prerun_subject = run_subject
    sort_started_at = time()
    path,shouldSkip,rule_name = sort_single_bug(
        base_dir=get_sort_repo_dir(),
        run_subject=run_subject,
        safe_dir="bug_reports/safe",
    )
    sorting_elapsed_seconds = time() - sort_started_at
    print(f"Sorting time: {sorting_elapsed_seconds:.2f}s")
    print(f"Matching rule folder: {path}")
    
    #Skip minimization if shouldSkip is True
    if shouldSkip:
        true_minification_started_at = time()
        run_result, _ = test_combination(target_browser.getDriver(), run_subject)
        true_minification_elapsed_seconds = time() - true_minification_started_at
        return (
            run_subject,
            run_result,
            prerun_subject,
            path,
            shouldSkip,
            rule_name,
            sorting_elapsed_seconds,
            true_minification_elapsed_seconds,
        )

    stepsFactory = MinifyStepFactory()
    # Keep applying minimization steps until no more are available
    true_minification_started_at = time()
    while True:
        # Get the next candidate minimized version of run_subject
        proposed_run_subject = stepsFactory.next_minimization_step(run_subject)
        # If there are no more steps, exit the loop
        if proposed_run_subject is None:
            # Break out when minimization can't shrink the subject further
            break
        
        # Test the proposed minimized subject in the target browser
        run_result, *_ = test_combination(target_browser.getDriver(), proposed_run_subject)
        # If the minimized subject still triggers the bug, accept it as the new subject
        if run_result.isBug():
            run_subject = proposed_run_subject

    # Create final representations of minified files
    run_result, _ = test_combination(target_browser.getDriver(), run_subject)
    true_minification_elapsed_seconds = time() - true_minification_started_at
    return (
        run_subject,
        run_result,
        prerun_subject,
        path,
        shouldSkip,
        rule_name,
        sorting_elapsed_seconds,
        true_minification_elapsed_seconds,
    )


def find_bugs(counter):
    target_browser = TargetBrowser()
    safe_dir = "bug_reports/safe"
    os.makedirs(safe_dir, exist_ok=True)
    write_run_summary(counter)

    def safe_count():
        return sum(
            1 for name in os.listdir(safe_dir)
            if name.endswith(".pkl")
        )

    while safe_count() < 50 and counter.should_continue():
        run_subject = generate_run_subject()
        run_result, test_filepath = test_combination(
            target_browser.getDriver(),
            run_subject,
            keep_file=True
        )

        if not run_result.isBug():
            print(f"Filling safe set: {safe_count() + 1}/50")
            pickle_addr = os.path.join(safe_dir, f"safe_{int(time() * 1000)}.pkl")
            with open(pickle_addr, "wb") as f:
                pickle.dump(run_subject, f)

        remove_file(test_filepath)
        counter.incTests()
        write_run_summary(counter)
        output = counter.getStatusString()
        if output:
            print(output)
            
    target_browser = TargetBrowser()

    while counter.should_continue():

        # Stage 1 - Generate & Test
        run_subject = generate_run_subject()
        (run_result, test_filepath) = test_combination(target_browser.getDriver(), run_subject, keep_file=True)

        if not run_result.isBug():
            counter.incSuccess()

        else:
            # Stage 2 - Minifying Bug
            print("Bug found. Minifying...")
            prerun_subject = run_subject
            minify_started_at = time()
            (
                minified_run_subject,
                minified_run_result,
                prerun_subject,
                path,
                shouldSkip,
                rule_name,
                sorting_elapsed_seconds,
                true_minification_elapsed_seconds,
            ) = minify(target_browser, prerun_subject)
            minify_elapsed_seconds = time() - minify_started_at
            counter.addMinifyTime(minify_elapsed_seconds)
            counter.addSortingTime(sorting_elapsed_seconds)
            counter.addTrueMinificationTime(true_minification_elapsed_seconds)
            print(
                f"Minify time: {minify_elapsed_seconds:.2f}s "
                f"(total {counter.total_minify_seconds:.2f}s)"
            )
            print(
                f"Sorting time: {sorting_elapsed_seconds:.2f}s "
                f"(total {counter.total_sorting_seconds:.2f}s)"
            )
            print(
                f"True minification time: {true_minification_elapsed_seconds:.2f}s "
                f"(total {counter.total_true_minification_seconds:.2f}s)"
            )
            print(f"Skip rule: {'skipped' if shouldSkip else 'not skipped'}")
            print(f"Rule name: {rule_name}")
            # Save bug report that matches a rule 
            if shouldSkip:
                save_bug_report(
                    variants=[],
                    minified_run_subject=minified_run_subject,
                    run_result=minified_run_result,
                    original_filepath=test_filepath,
                    prerun_subject=prerun_subject,
                    path=path,
                    shouldSkip=shouldSkip,
                    rule_name=rule_name,
                    sorting_seconds=sorting_elapsed_seconds,
                    true_minification_seconds=true_minification_elapsed_seconds,
                )

            # False Positive Detection
            if not minified_run_result.isBug():
                print("False positive (could not reproduce)")
                counter.incNoRepro()
            elif minified_run_result.type == BugType.LAYOUT and len(minified_run_subject.modified_styles.map) == 0:
                print("False positive (no modified styles)")
                counter.incNoMod()

            else:
                counter.incError()

                # Stage 3 - Test Variants
                variants = test_variants(minified_run_subject)

                url = save_bug_report(
                    variants,
                    minified_run_subject,
                    minified_run_result,
                    test_filepath,
                    prerun_subject,
                    path=path,
                    shouldSkip=shouldSkip,
                    rule_name=rule_name,
                    sorting_seconds=sorting_elapsed_seconds,
                    true_minification_seconds=true_minification_elapsed_seconds,
                )
                print(f"Bug report saved: {url}")

        counter.incTests()
        write_run_summary(counter)
        output = counter.getStatusString()
        if output:
            print(output)

        # Clean Up
        remove_file(test_filepath)


DEFAULT_CONFIG_FILE = "./config/preset-default.config.json"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""find bugs in browser layout calculation - run forever unless specified otherwise\n\nexamples: \n    compare.py -b 1         # Find one bug and quit \n    compare.py -t 2000      # Run 2000 tests and quit""")
    parser.add_argument("-b", "--bug-limit", help="quit after finding this many bugs", type=int, default=0)
    parser.add_argument("-t", "--test-limit", help="quit after running this many tests", type=int, default=0)
    parser.add_argument("-l", "--crash-limit", help="quit after crashing this many times", type=int, default=1)
    parser.add_argument("-c", "--config-file", help="path to config file to use", type=str, default=DEFAULT_CONFIG_FILE)
    args = parser.parse_args()

    # Initialize Config
    print(f"Using config file {args.config_file}")
    conf = parse_config(args.config_file)
    Config(conf)

    # Logging - Target Variant
    target_variant = getTargetVariant()
    print(f"Using target variant \"{target_variant}\"")

    counter = Counter(bug_limit=args.bug_limit, test_limit=args.test_limit, crash_limit=args.crash_limit)

    while counter.should_continue():
        try:
            find_bugs(counter)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc = {
                "etype": exc_type,
                "value": exc_value,
                "traceback": exc_traceback,
            }
            counter.incCrash(exc=exc)
            write_run_summary(counter)

    write_run_summary(counter)

    if counter.num_crash > 0:
        print(f"Number of crashes: {counter.num_crash}\nCrash Errors:\n")
        for exc in counter.crash_exceptions:
            traceback.print_exception(exc["etype"], exc["value"], exc["traceback"])
            print("-"*60 + "\n")


