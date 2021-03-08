#!/usr/bin/env python3

import os, sys, traceback, argparse
from layout_tester import test_combination
from style_log_generator import generate_layout_tree, generate_style_log
from html_file_generator import remove_file
from minify_test_file import minify
from bug_report_helper import save_bug_report
from variant_tester import test_variants
from test_subject import TestSubject
from element_tree import ElementTree
from style_map import StyleMap
from webdrivers import chrome
from counter import Counter


def find_bugs(counter):

    chrome_webdriver = chrome.getWebDriver()

    while counter.should_continue():

        # Stage 1 - Generate & Test
        body = generate_layout_tree()
        base_style_log = generate_style_log(body, 0.1, is_base=True)
        modified_style_log = generate_style_log(body, 0.1, is_base=False)

        test_subject = TestSubject(ElementTree(body), StyleMap(base_style_log), StyleMap(modified_style_log))
        (no_differences, differences, test_filepath) = test_combination(chrome_webdriver, test_subject, keep_file=True)

        if no_differences:
            counter.incSuccess()

        else:
            # Stage 2 - Minifying Bug
            print("Found bug. Minifying...")
            (minified_test_subject, minified_differences) = minify(chrome_webdriver, test_subject)

            # False Positive Detection
            if minified_differences is None:
                print("False positive (could not reproduce)")
                counter.incNoRepro()
            elif len(minified_test_subject.modified_styles.map) == 0:
                print("False positive (no modified styles)")
                counter.incNoMod()

            else:
                counter.incError()

                # Stage 3 - Test Variants
                print("Minified bug. Testing variants...")
                variants = test_variants(minified_test_subject)

                print("Variants tested. Saving bug report...")
                url = save_bug_report(
                    variants,
                    minified_test_subject,
                    minified_differences,
                    test_filepath
                )
                print(url)

        counter.incTests()
        output = counter.getStatusString()
        if output:
            print(output)

        # Clean Up
        remove_file(test_filepath)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="""find bugs in browser layout calculation - run forever unless specified otherwise\n\nexamples: \n    compare.py -b 1         # Find one bug and quit \n    compare.py -t 2000      # Run 2000 tests and quit""")
    parser.add_argument("-v", "--verbose", help="increase output verbosity (repeatable argument -v, -vv, -vvv, -vvvv)", action="count", default=0)
    parser.add_argument("-b", "--bug-limit", help="quit after finding this many bugs", type=int, default=0)
    parser.add_argument("-t", "--test-limit", help="quit after running this many tests", type=int, default=0)
    args = parser.parse_args()

    counter = Counter(bug_limit=args.bug_limit, test_limit=args.test_limit)

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

    if counter.num_crash > 0:
        print("Crash Errors:\n")
        for exc in counter.crash_exceptions:
            traceback.print_exception(exc["etype"], exc["value"], exc["traceback"])
            print("-"*60 + "\n")

