from file_config import FileConfig
from test_config import TestConfig
from test_subject import TestSubject
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from html_file_generator import get_file_path
from layout_comparer import compare_layout
from web_page_creation.create import save_as_web_page
import os

inspector_file = "http://localhost:8000/inspector.html"
cwd = os.getcwd()
cwd = cwd.replace("\\", "/")


# Returns (differencesIsNone, differencesList, fileName)
def test_combination(test_config: TestConfig, test_subject: TestSubject):
    file_config = FileConfig()
    test_filepath, test_filename = get_file_path(file_config.layout_file_dir, test_config.timestamp)
    save_as_web_page(test_subject, test_filepath)

    test_web_page = f"http://localhost:8000/{file_config.relative_url_path}/{test_filename}"

    differences = run_test_on_page(test_web_page, test_config, test_subject)

    return (differences is None), differences, test_filepath


def run_test_on_page(test_url, test_config: TestConfig, test_subject: TestSubject):

    test_config.webdriver.get(f"{test_url}")
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
        # WebDriverWait(test_config.webdriver, timeout, poll_frequency=poll_frequency).until(lambda d: d.execute_script("return typeof(inspectorTools) !== 'undefined'"))

        # Wait until page is loaded
        # WebDriverWait(test_config.webdriver, timeout, poll_frequency=poll_frequency).until(lambda d: d.execute_script("return inspectorTools.isPageLoaded();"))

        # Make the style changes
        test_config.webdriver.execute_script("makeStyleChanges()")

        # Measure the elements
        base_values = test_config.webdriver.execute_script("return outputElementDimensions()")

        # Reload the page exactly as it is (including style changes)
        test_config.webdriver.execute_script("reload()")

        # Measure the elements again
        modified_values = test_config.webdriver.execute_script("return outputElementDimensions()")

    except TimeoutException:
        print("Failed to load test page due to timeout")

    differences = compare_layout(base_values, modified_values)

    return differences

