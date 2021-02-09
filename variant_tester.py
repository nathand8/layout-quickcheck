from web_page_creation.create import save_as_web_page
from html_file_generator import get_file_path, remove_file
from file_config import FileConfig
from layout_tester import run_test_using_js_diff_detect, test_combination
from webdrivers import chrome, firefox
from test_subject import TestSubject



def get_variant(webdriver, bug_gone, description, diff_method="Python"):

    browser_name = webdriver.capabilities['browserName']
    browser_version = webdriver.capabilities['browserVersion']
    window_size = webdriver.get_window_size()
    return {
        "description": description,
        "bug_detected": not bug_gone,
        "browser": browser_name,
        "browser_version": browser_version,
        "window_size": window_size,
        "diff_method": diff_method
    }


def test_variants(test_subject: TestSubject):

    variants = []

    # Regular run
    description = "Default Variant"
    chrome_webdriver = chrome.getWebDriver()
    bug_gone, *_ = test_combination(chrome_webdriver, test_subject)
    variants.append(get_variant(chrome_webdriver, bug_gone, description))
    chrome_webdriver.close()

    # Smaller Window
    description = "Smaller Window Size"
    chrome_webdriver = chrome.getWebDriver(window_width=500, window_height=500)
    bug_gone, *_ = test_combination(chrome_webdriver, test_subject)
    variants.append(get_variant(chrome_webdriver, bug_gone, description))
    chrome_webdriver.close()

    # Larger Window Size
    description = "Larger Window Size"
    chrome_webdriver = chrome.getWebDriver(window_width=2400, window_height=2400)
    bug_gone, *_ = test_combination(chrome_webdriver, test_subject)
    variants.append(get_variant(chrome_webdriver, bug_gone, description))
    chrome_webdriver.close()

    # Using JS Change Detection
    description = "JavaScript Difference Detection"
    chrome_webdriver = chrome.getWebDriver()

    file_config = FileConfig()
    test_filepath, test_filename = get_file_path(file_config.layout_file_dir)
    save_as_web_page(test_subject, test_filepath)
    test_web_page = f"http://localhost:8000/{file_config.relative_url_path}/{test_filename}"
    differences = run_test_using_js_diff_detect(test_web_page, chrome_webdriver, slow=True)
    bug_gone = differences is None

    variants.append(get_variant(chrome_webdriver, bug_gone, description, diff_method="JavaScript"))
    remove_file(test_filepath)
    chrome_webdriver.close()

    # Run in Firefox
    description = "Firefox Browser"
    firefox_webdriver = firefox.getWebDriver()
    bug_gone, *_ = test_combination(firefox_webdriver, test_subject)
    variants.append(get_variant(firefox_webdriver, bug_gone, description))
    firefox_webdriver.close()

    return variants
