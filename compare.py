#!/usr/bin/env python3
# flake8: noqa: E402
from variant_tester import test_variants
from dotenv import load_dotenv

load_dotenv()

import os
from layout_tester import test_combination
from style_log_generator import generate_layout_tree, generate_style_log
from html_file_generator import remove_file
from minify_test_file import minify
from bug_report_helper import save_bug_report
from test_subject import TestSubject
from element_tree import ElementTree
from style_map import StyleMap
from webdrivers import chrome
from counter import Counter


counter = Counter()

chrome_webdriver = chrome.getWebDriver()

servo_session_key = None
servo_retry_failures = 0

required_failure_count = int(os.environ.get("FAILURE_COUNT", 0))
is_based_on_failure = required_failure_count > 0
required_test_count = int(os.environ.get("TEST_COUNT", 0))
is_based_on_test_count = required_test_count > 0


def should_continue():
    if is_based_on_failure:
        return counter.num_error < required_failure_count
    elif is_based_on_test_count:
        return counter.num_tests < required_test_count
    else:
        return True


while should_continue():
    body = generate_layout_tree()
    base_style_log = generate_style_log(body, 0.1, is_base=True)
    modified_style_log = generate_style_log(body, 0.1, is_base=False)
    test_subject = TestSubject(ElementTree(body), StyleMap(base_style_log), StyleMap(modified_style_log))

    (no_differences, differences, test_filepath) = test_combination(chrome_webdriver, test_subject, keep_file=True)

    if no_differences:
        counter.incSuccess()
    else:

        # TODO: Force another test with long waits to ensure this is a bug

        print("Found failing test. Minimizing...")
        (
            minified_test_subject,
            minified_differences,
        ) = minify(chrome_webdriver, test_subject)

        if minified_differences is None:
            print("Can't reproduce the problem after minimizing...")
            counter.incNoRepro()
        elif len(minified_test_subject.modified_styles.map) == 0:
            counter.incNoMod()
        else:
            counter.incError()
            print("Testing variants of setup...")
            variants = test_variants(minified_test_subject)
            print("Saving bug report...")
            save_bug_report(
                variants,
                minified_test_subject,
                minified_differences,
                test_filepath
            )



    counter.incTests()
    output = counter.getStatusString()
    if output:
        print(output)


    # Clean up the test file
    remove_file(test_filepath)



