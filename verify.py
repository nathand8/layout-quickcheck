from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from html_file_generator import save_file, get_file_path
from style_log_applier import apply_log
from layout_comparer import compare_layout
import os
import time

# Returns (differencesIsNone, differencesList, fileName)
def test_combination(chrome_webdriver, test_web_page, modified_style_log):

    chrome_webdriver.get(f"{test_web_page}")
    try:
        timeout = 5

        # Wait until the inspectorTools has loaded
        WebDriverWait(chrome_webdriver, timeout).until(lambda d: d.execute_script("return typeof(inspectorTools) !== 'undefined'"))

        # Wait until page is loaded
        WebDriverWait(chrome_webdriver, timeout).until(lambda d: d.execute_script("return inspectorTools.isPageLoaded();"))

        chrome_webdriver.execute_script(
            "inspectorTools.modifyStyles(arguments[0])", modified_style_log
        )
        base_values = chrome_webdriver.execute_script(
            "return inspectorTools.outputElementDimensions()"
        )
        chrome_webdriver.execute_script(
            "inspectorTools.loadCurrentStateFresh()"
        )
        modified_values = chrome_webdriver.execute_script(
            "return inspectorTools.outputElementDimensions()"
        )
    except TimeoutException:
        print("Failed to load test page due to timeout")

    differences = compare_layout(base_values, modified_values)

    return differences


if __name__ == "__main__":

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_webdriver = WebDriver(
        executable_path=os.environ.get("CHROME_DRIVER_PATH"), options=chrome_options
    )

    browser_version = chrome_webdriver.capabilities['browserVersion']
    driver_version = chrome_webdriver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print("Chrome Version   :", browser_version)
    print("WebDriver Version:", driver_version)

    url = "http://localhost:8000/odd-behavior-bugs/bug-report-2021-01-27-05-26-52-274354-minified-86/bug.html"
    modified_styles = {"03e40bd619664c4fb84c60028fd23ce0": {"margin-left": "-20px", "margin-top": "auto", "margin-block-start": "20px"}}

    differences = test_combination(chrome_webdriver, url, modified_styles)

    print("differences:", differences)
