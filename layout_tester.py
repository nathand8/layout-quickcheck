from file_config import FileConfig
from test_subject import TestSubject
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from html_file_generator import get_file_path, remove_file
from layout_comparer import compare_layout
from web_page_creation.create import save_as_web_page
import os
import time

inspector_file = "http://localhost:8000/inspector.html"
cwd = os.getcwd()
cwd = cwd.replace("\\", "/")


# Returns (differencesIsNone, differencesList, fileName)
def test_combination(webdriver, test_subject: TestSubject, slow=False):
    file_config = FileConfig()
    test_filepath, test_filename = get_file_path(file_config.layout_file_dir)
    save_as_web_page(test_subject, test_filepath)

    test_web_page = f"http://localhost:8000/{file_config.relative_url_path}/{test_filename}"

    differences = run_test_on_page(test_web_page, webdriver, slow=slow)
    
    return (differences is None), differences, test_filepath


def run_test_on_page(test_url, webdriver, slow=False):

    webdriver.get(f"{test_url}")
    base_values = {}
    modified_values = {}
    try:
        timeout = 5
        poll_frequency = 0.001
        # Performance on CADE machines (Jan 27, 2020)
        # poll_frequency = 0.0001, inspectorTools ~ 2.6ms, pageLoad ~ 5.6ms
        # poll_frequency = 0.001, inspectorTools ~ 2.8ms, pageLoad ~ 6.0ms
        # poll_frequency = 0.01, inspectorTools ~ 3.2ms, pageLoad ~ 15ms
        # poll_frequency = 0.1, inspectorTools ~ 3.0ms, pageLoad ~ 105ms

        # Wait until inspectorTools is loaded
        # WebDriverWait(webdriver, timeout, poll_frequency=poll_frequency).until(lambda d: d.execute_script("return typeof(inspectorTools) !== 'undefined'"))

        # Wait until page is loaded
        # WebDriverWait(webdriver, timeout, poll_frequency=poll_frequency).until(lambda d: d.execute_script("return inspectorTools.isPageLoaded();"))

        # Wait until body element is loaded
        WebDriverWait(webdriver, timeout, poll_frequency=poll_frequency).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        if slow: time.sleep(0.5)

        # Make the style changes
        webdriver.execute_script("makeStyleChanges()")

        if slow: time.sleep(0.5)

        # Measure the elements
        base_values = webdriver.execute_script("return outputElementDimensions()")

        if slow: time.sleep(0.5)

        # Reload the page exactly as it is (including style changes)
        webdriver.execute_script("reload()")

        if slow: time.sleep(0.5)

        # Measure the elements again
        modified_values = webdriver.execute_script("return outputElementDimensions()")

    except TimeoutException:
        print("Failed to load test page due to timeout")

    differences = compare_layout(base_values, modified_values)

    return differences


def run_test_using_js_diff_detect(test_url, webdriver, slow=False):

    webdriver.get(f"{test_url}")
    try:
        timeout = 5
        poll_frequency = 0.001

        # Wait until body element is loaded
        WebDriverWait(webdriver, timeout, poll_frequency=poll_frequency).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        if slow: time.sleep(0.5)

        # Make the style changes
        differences = webdriver.execute_script("return recreateTheProblem()")
        return differences

    except TimeoutException:
        print("Failed to load test page due to timeout")
        return None


