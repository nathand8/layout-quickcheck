#!/usr/bin/env python3
# flake8: noqa: E402
from dotenv import load_dotenv

load_dotenv()

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
from layout_tester import test_combination
from style_log_generator import generate_layout_tree, generate_style_log
from html_file_generator import remove_file
from minify_test_file import minify
from bug_report_helper import save_bug_report
from test_config import TestConfig
from test_subject import TestSubject
from style_map import StyleMap
from datetime import datetime
import atexit


timestamp_format = "%Y-%m-%d-%H-%M-%S-%f"


num_tests = 0
num_successful = 0
num_error = 0
num_cant_reproduce = 0

chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_webdriver = WebDriver(
    executable_path=os.environ.get("CHROME_DRIVER_PATH"), options=chrome_options
)

servo_session_key = None
servo_retry_failures = 0

required_failure_count = int(os.environ.get("FAILURE_COUNT", 0))
is_based_on_failure = required_failure_count > 0
required_test_count = int(os.environ.get("TEST_COUNT", 0))
is_based_on_test_count = required_test_count > 0


def should_continue():
    if is_based_on_failure:
        return num_error < required_failure_count
    elif is_based_on_test_count:
        return num_tests < required_test_count
    else:
        return True


while should_continue():
    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime(timestamp_format)
    body = generate_layout_tree()
    base_style_log = generate_style_log(body, 0.1, is_base=True)
    modified_style_log = generate_style_log(body, 0.1, is_base=False)
    test_config = TestConfig(chrome_webdriver, formatted_timestamp)
    test_subject = TestSubject(body, StyleMap(base_style_log), StyleMap(modified_style_log))

    (no_differences, differences, test_filepath) = test_combination(test_config, test_subject)

    if no_differences:
        num_successful += 1
    else:

        # TODO: Force another test with long waits to ensure this is a bug

        print("Found failing test. Minimizing...")
        (
            minified_test_subject,
            minified_differences,
        ) = minify(test_config, test_subject)

        if differences is None:
            print("Can't reproduce the problem after minimizing...")
            num_cant_reproduce += 1
        else:
            num_error += 1

        save_bug_report(
            test_config,
            minified_test_subject,
            minified_differences,
            test_filepath,
            cant_reproduce = differences is None
        )

    num_tests += 1

    print(f"Success: {num_successful}; Failed: {num_error}; Can't Reproduce: {num_cant_reproduce}")

    # Clean up the test file
    remove_file(test_filepath)



def terminate_browsers():
    print("closing browsers")
    if chrome_webdriver is not None:
        print("Closing Chrome")
        chrome_webdriver.close()


atexit.register(terminate_browsers)
