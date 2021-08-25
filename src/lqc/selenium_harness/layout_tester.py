from lqc.generate.html_file_generator import remove_file
from lqc.generate.web_page.run_subject_converter import saveTestSubjectAsWebPage
from lqc.model.run_subject import RunSubject
from lqc.util.layout_comparer import compare_layout
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

PAGE_CRASH = "Page Crashed"

# Returns (differencesIsNone, differencesList, fileName)
# @param keep_file - keep the intermediate file, the caller is responsible for cleanup
def test_combination(webdriver, run_subject: RunSubject, slow=False, keep_file=False):
    test_filepath, test_url = saveTestSubjectAsWebPage(run_subject)

    differences = run_test_on_page(test_url, webdriver, slow=slow)
    no_bug = differences is None
    
    if not keep_file:
        remove_file(test_filepath)
        return no_bug, differences, None
    else:
        return no_bug, differences, test_filepath


def run_test_on_page(test_url, webdriver, slow=False):

    base_values = {}
    modified_values = {}
    try:
        webdriver.get(f"{test_url}")
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
    except WebDriverException as e:
        if "page crash" in str(e).lower():
            return PAGE_CRASH
        else:
            raise

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
        return differences == [], differences

    except TimeoutException:
        print("Failed to load test page due to timeout")
        return None
    except WebDriverException:
        return PAGE_CRASH

