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

    differences = run_test_using_js_diff_detect(test_url, webdriver, slow=slow)
    no_bug = not differences
    
    if not keep_file:
        remove_file(test_filepath)
        return no_bug, differences, None
    else:
        return no_bug, differences, test_filepath


def run_test_using_js_diff_detect(test_url, webdriver, slow=False):

    webdriver.get(f"{test_url}")
    try:
        timeout = 5
        poll_frequency = 0.001

        # Wait until body element is loaded
        WebDriverWait(webdriver, timeout, poll_frequency=poll_frequency).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        if slow: time.sleep(0.5)

        # Make the style changes
        return webdriver.execute_script("return recreateTheProblem()")

    except TimeoutException:
        print("Failed to load test page due to timeout")
        return None
    except WebDriverException:
        return PAGE_CRASH

