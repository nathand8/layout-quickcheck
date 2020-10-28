#!/usr/bin/env python3

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import os
from html_file_generator import generate_html_file, save_modified
from layout_comparer import compare_layout
from style_log_generator import generate_layout_tree, generate_style_log
from style_log_applier import apply_log
import atexit
from dotenv import load_dotenv

load_dotenv()

cwd = os.getcwd()
cwd = cwd.replace('\\', '/')
layout_file_dir = os.environ.get('LAYOUT_FILE_DIR', f'{cwd}/layoutfiles')
is_manual_test = False

if not os.path.exists(layout_file_dir):
    os.makedirs(layout_file_dir)

inspector_file = 'http://localhost:8000/inspector.html'
num_tests = 0
num_successful = 0
num_error = 0

chrome_options = ChromeOptions()
chrome_webdriver = WebDriver(
    executable_path=os.environ.get('CHROME_DRIVER_PATH'),
    options=chrome_options)

servo_session_key = None
servo_retry_failures = 0

while num_tests < 1000:
    body = generate_layout_tree()
    base_style_log = generate_style_log(body, 0.05)
    modified_style_log = generate_style_log(body, 0.01)
    applied_layout = apply_log(body, base_style_log)
    test_file_name, test_timestamp = generate_html_file(layout_file_dir, applied_layout)
    test_web_page = f'http://localhost:8000/layoutfiles/{test_file_name}'

    chrome_webdriver.get(f'{inspector_file}?url={test_web_page}')
    try:
        timeout = 5
        iframe_ready = EC.text_to_be_present_in_element((By.ID, 'status'),
                                                        'Ready')
        WebDriverWait(chrome_webdriver, timeout).until(iframe_ready)

        chrome_webdriver.execute_script(
            'inspectorTools.modifyStyles(arguments[0])',
            modified_style_log
        )
        chrome_values = chrome_webdriver.execute_script(
            'return inspectorTools.outputIframeContents()')
        chrome_html_output = chrome_webdriver.execute_script(
            'return inspectorTools.getHtml()'
        )
    except TimeoutException:
        print('Failed to load test page due to timeout')

    modified_test_file_name = save_modified(
        layout_file_dir, test_timestamp, chrome_html_output)
    modified_test_web_page = \
        f'http://localhost:8000/layoutfiles/{modified_test_file_name}'

    chrome_webdriver.get(f'{inspector_file}?url={modified_test_web_page}')
    try:
        timeout = 5
        iframe_ready = EC.text_to_be_present_in_element((By.ID, 'status'),
                                                        'Ready')
        WebDriverWait(chrome_webdriver, timeout).until(iframe_ready)

        modified_values = chrome_webdriver.execute_script(
            'return inspectorTools.outputIframeContents()')
    except TimeoutException:
        print('Failed to load test page due to timeout')

    differences = compare_layout(chrome_values, modified_values)

    if differences is None:
        num_successful += 1
    else:
        print('Differences: ')
        print(differences)
        print(f'Failed file: {test_web_page}')
        print(body)
        print(base_style_log)
        print(modified_style_log)
        # print(chrome_values)
        # print(modified_values)
        num_error += 1
        break

    num_tests += 1

    print(f'Finished test {num_tests}')
    print(f'Success: {num_successful}; Failed: {num_error}')


def terminate_browsers():
    print('closing browsers')
    if chrome_webdriver is not None:
        print('Closing Chrome')
        chrome_webdriver.close()


atexit.register(terminate_browsers)
