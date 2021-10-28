from lqc.generate.html_file_generator import remove_file
from lqc.generate.web_page.run_subject_converter import saveTestSubjectAsWebPage
from lqc.model.run_result import RunResult, RunResultCrash, RunResultLayoutBug, RunResultPass
from lqc.model.run_subject import RunSubject
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time


# Returns (differencesIsNone, differencesList, fileName)
# @param keep_file - keep the intermediate file, the caller is responsible for cleanup
def test_combination(webdriver, run_subject: RunSubject, slow=False, keep_file=False):
    test_filepath, test_url = saveTestSubjectAsWebPage(run_subject)

    run_result = run_test_using_js_diff_detect(test_url, webdriver, slow=slow)
    
    if not keep_file:
        remove_file(test_filepath)
        return run_result, None
    else:
        return run_result, test_filepath


def run_test_using_js_diff_detect(test_url, webdriver, slow=False) -> RunResult:

    webdriver.get(f"{test_url}")
    try:
        timeout = 5
        poll_frequency = 0.001

        # Wait until body element is loaded
        WebDriverWait(webdriver, timeout, poll_frequency=poll_frequency).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        if slow: time.sleep(0.5)

        # Make the style changes
        results =  webdriver.execute_script("return recreateTheProblem()")
        if results and len(results) > 0:
            return RunResultLayoutBug(results)
        else:
            return RunResultPass()

    except TimeoutException:
        print("Failed to load test page due to timeout")
        return None
    except WebDriverException:
        return RunResultCrash()

