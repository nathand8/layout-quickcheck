#!/usr/bin/env python3
# flake8: noqa: E402
from dotenv import load_dotenv

load_dotenv()

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
from layout_tester import test_combination
from style_log_generator import generate_layout_tree, generate_style_log
from minify_test_file import minify
from bug_report_helper import save_bug_report
from test_config import TestConfig
from test_subject import TestSubject
from datetime import datetime
import atexit


cwd = os.getcwd()
cwd = cwd.replace("\\", "/")
layout_file_dir = os.environ.get("LAYOUT_FILE_DIR", f"{cwd}/layoutfiles")
bug_report_file_dir = os.environ.get("BUG_REPORT_FILE_DIR", f"{cwd}/bugreportfiles")
is_manual_test = False
timestamp_format = "%Y-%m-%d-%H-%M-%S-%f"

if not os.path.exists(layout_file_dir):
    os.makedirs(layout_file_dir)
if not os.path.exists(bug_report_file_dir):
    os.makedirs(bug_report_file_dir)

num_tests = 0
num_successful = 0
num_error = 0

chrome_options = ChromeOptions()
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

    (is_success, differences, test_file_name,) = test_combination(
        chrome_webdriver,
        formatted_timestamp,
        "",
        body,
        base_style_log,
        modified_style_log,
    )

    if is_success:
        num_successful += 1
    else:
        test_config = TestConfig(chrome_webdriver, formatted_timestamp)
        test_subject = TestSubject(body, base_style_log, modified_style_log)
        print("Found failing test. Minimizing...")
        (
            minified_test_subject,
            minified_postfix,
            minified_differences,
        ) = minify(test_config, test_subject)
        save_bug_report(
            bug_report_file_dir,
            layout_file_dir,
            formatted_timestamp,
            minified_test_subject.html_tree,
            minified_test_subject.base_styles,
            minified_test_subject.modified_styles,
            minified_postfix,
            minified_differences,
        )
        num_error += 1

    num_tests += 1

    print(f"Success: {num_successful}; Failed: {num_error}")


def terminate_browsers():
    print("closing browsers")
    if chrome_webdriver is not None:
        print("Closing Chrome")
        chrome_webdriver.close()


atexit.register(terminate_browsers)
