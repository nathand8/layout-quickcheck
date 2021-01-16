from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from html_file_generator import save_file
from style_log_applier import apply_log
from layout_comparer import compare_layout
import os

inspector_file = "http://localhost:8000/inspector.html"
cwd = os.getcwd()
cwd = cwd.replace("\\", "/")
layout_file_dir = os.getenv("LAYOUT_FILE_DIR", f"{cwd}/layoutfiles")
relative_layout_path = os.getenv("RELATIVE_LAYOUT_PATH", "layoutfiles")

# Wrapper around test_combination that uses a TestSubject
# test_subject of type TestSubject
def test_combination_wrapper(test_config, test_subject):
    return test_combination(test_config.webdriver, test_config.timestamp, test_config.postfix, test_subject.html_tree, test_subject.base_styles, test_subject.modified_styles)

# Returns (differencesIsNone, differencesList, fileName)
def test_combination(
    chrome_webdriver, test_timestamp, postfix, body, base_style_log, modified_style_log
):
    applied_layout = apply_log(body, base_style_log, modified_style_log)
    test_file_name = save_file(layout_file_dir, test_timestamp, applied_layout, postfix)
    test_web_page = f"http://localhost:8000/{relative_layout_path}/{test_file_name}"

    chrome_webdriver.get(f"{inspector_file}?url={test_web_page}")
    try:
        timeout = 5
        iframe_ready = EC.text_to_be_present_in_element((By.ID, "status"), "Ready")
        WebDriverWait(chrome_webdriver, timeout).until(iframe_ready)

        chrome_webdriver.execute_script(
            "inspectorTools.modifyStyles(arguments[0])", modified_style_log
        )
        base_values = chrome_webdriver.execute_script(
            "return inspectorTools.outputIframeContents()"
        )
        chrome_webdriver.execute_script(
            "inspectorTools.loadCurrentStateFresh()"
        )
        modified_values = chrome_webdriver.execute_script(
            "return inspectorTools.outputIframeContents()"
        )
    except TimeoutException:
        print("Failed to load test page due to timeout")

    differences = compare_layout(base_values, modified_values)

    return (differences is None), differences, test_file_name
