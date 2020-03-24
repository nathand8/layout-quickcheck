from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from sys import argv
import os
import subprocess
import json

if len(argv) <= 1:
  print('Please specify a test web page')
  exit(1)


def parse_servo_json(servo_json):
  root = servo_json['post']

  def recurse(element):
    position = element['data']['base']['position']
    values = {
      'x': position['start']['i'] / 60,
      'y': position['start']['b'] / 60,
      'width': position['size']['inline'] / 60,
      'height': position['size']['block'] / 60
    }

    values['children'] = list(map(recurse, element['data']['base']['children']))

    return values
  
  return recurse(root['children'][0])



inspector_file = 'file:///C:/Users/William/code/school/project/jsInspector/inspector.html'
test_web_page = argv[1]
servo_layout_trace_file = 'C:\\Users\\William\\code\\school\\servo\\layout_trace-0.json'

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

subprocess.run(['C:\\Users\\William\\code\\school\\servo\\mach.bat', 'run',
                '--dev', '--', '-x', '--resolution', '800x600', 
                '--debug', 'trace-layout', test_web_page],
                cwd='C:\\Users\\William\\code\\school\\servo')

with open(servo_layout_trace_file, 'r') as layout_trace_file:
  servo_json = json.load(layout_trace_file)

os.remove(servo_layout_trace_file)

parsed_servo_json = parse_servo_json(servo_json)

print(parsed_servo_json)
