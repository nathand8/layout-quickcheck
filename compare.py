#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from sys import argv
import os
import subprocess
import json
from html_file_generator import generate_html_file
from layout_comparer import compare_layout
from servo_parser import parse_servo_json
import requests
import atexit
from time import sleep
import glob

cwd = os.getcwd()
cwd = cwd.replace('\\', '/')
layout_file_dir = os.environ.get('LAYOUT_FILE_DIR', f'{cwd}/layoutfiles')
servo_dir = os.environ.get('SERVO_DIRECTORY', f'{cwd}/../servo')
mach_extension = '.bat' if os.name == 'nt' else ''
is_manual_test = False

if len(argv) <= 1:
    if not os.path.exists(layout_file_dir):
        os.makedirs(layout_file_dir)
else:
    test_web_page = argv[1]
    is_manual_test = True

inspector_file = f'file:///{cwd}/inspector.html'
num_tests = 0
num_successful = 0
num_error = 0

firefox_options = Options()
firefox_options.headless = True

firefox_webdriver = webdriver.Firefox(options=firefox_options)

servo_process = subprocess.Popen([
    f'{servo_dir}/mach{mach_extension}', 'run', '--dev', '--',
    '--webdriver=7002', '--user-stylesheet', f'{cwd}/css/firefox.css',
    '--resolution', '800x600', '--debug', 'trace-layout',
    'http://localhost:8000/knownbug.html'
],
                                 cwd=servo_dir)

servo_session_key = None
servo_retry_failures = 0

while servo_session_key is None:
    print(f'Waiting for servo to be ready (try {servo_retry_failures}')
    if servo_retry_failures > 12:
        exit(1)
    try:
        servo_session_res = requests.post('http://localhost:7002/session',
                                          json={})
        servo_session_key = servo_session_res.json()['value']['sessionId']
    except requests.exceptions.ConnectionError:
        servo_retry_failures += 1
        sleep(5)

while num_tests < 10 or (is_manual_test and num_tests < 1):
    if not is_manual_test:
        test_file_name = generate_html_file(layout_file_dir)
        test_web_page = f'file:///{layout_file_dir}/{test_file_name}'

    firefox_webdriver.get(f'{inspector_file}?url={test_web_page}')

    try:
        timeout = 5
        iframe_ready = EC.text_to_be_present_in_element((By.ID, 'status'),
                                                        'Ready')
        WebDriverWait(firefox_webdriver, timeout).until(iframe_ready)

        firefoxValues = firefox_webdriver.execute_script(
            'return outputIframeContents()')
    except TimeoutException:
        print('Failed to load test page due to timeout')

    # print(firefoxValues)

    servo_request = requests.post(
        f'http://localhost:7002/session/{servo_session_key}/url',
        json={'url': test_web_page})

    servo_trace_files = glob.glob(f'{servo_dir}/layout_trace*')
    if len(servo_trace_files) > 0:
        servo_layout_trace_file = max(servo_trace_files, key=os.path.getctime)

    if servo_layout_trace_file is not None:
        with open(servo_layout_trace_file, 'r') as layout_trace_file:
            servo_json = json.load(layout_trace_file)

        for trace_file in servo_trace_files:
            os.remove(trace_file)

    parsed_servo_json = parse_servo_json(servo_json)

    # print(parsed_servo_json)

    differences = compare_layout(firefoxValues, parsed_servo_json)

    if differences is None:
        num_successful += 1
    else:
        print('Differences: ')
        print(differences)
        print(f'Failed file: {test_web_page}')
        num_error += 1

    num_tests += 1

    print(f'Finished test {num_tests}')
    print(f'Success: {num_successful}; Failed: {num_error}')


def terminate_browsers():
    print('closing browsers')
    if firefox_webdriver is not None:
        print('Closing Firefox')
        firefox_webdriver.close()
    if servo_process is not None:
        print('Closing servo')
        servo_process.terminate()


atexit.register(terminate_browsers)
