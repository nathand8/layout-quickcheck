#!/usr/bin/env python3

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from sys import argv
import os
import subprocess
import json
from html_file_generator import generate_html_file
from layout_comparer import compare_layout
from servo_parser import parse_servo_json

cwd = os.getcwd()
cwd = cwd.replace('\\', '/')
layout_file_dir = os.environ.get('LAYOUT_FILE_DIR', f'{cwd}/layoutfiles')
servo_dir = os.environ.get('SERVO_DIRECTORY', f'{cwd}/../servo')
mach_extension = '.bat' if os.name == 'nt' else ''

if len(argv) <= 1:
    if not os.path.exists(layout_file_dir):
        os.makedirs(layout_file_dir)

    test_file_name = generate_html_file(layout_file_dir)
    test_web_page = f'file:///{layout_file_dir}/{test_file_name}'
else:
    test_web_page = argv[1]

inspector_file = f'file:///{cwd}/inspector.html'
servo_layout_trace_file = f'{servo_dir}/layout_trace-0.json'

browser = webdriver.Firefox()

browser.get(f'{inspector_file}?url={test_web_page}')

try:
    timeout = 5
    iframe_ready = EC.text_to_be_present_in_element((By.ID, 'status'), 'Ready')
    WebDriverWait(browser, timeout).until(iframe_ready)

    firefoxValues = browser.execute_script('return outputIframeContents()')
except TimeoutException:
    print('Failed to load test page due to timeout')

browser.close()

print(firefoxValues)

subprocess.run([
    f'{servo_dir}/mach{mach_extension}', 'run', '--dev', '--', '-x',
    '--user-stylesheet', f'{cwd}/css/firefox.css', '--resolution', '800x600',
    '--debug', 'trace-layout', test_web_page
],
               cwd=servo_dir)

with open(servo_layout_trace_file, 'r') as layout_trace_file:
    servo_json = json.load(layout_trace_file)

os.remove(servo_layout_trace_file)

parsed_servo_json = parse_servo_json(servo_json)

print(parsed_servo_json)

differences = compare_layout(firefoxValues, parsed_servo_json)

print('Differences: ')
print(differences)
