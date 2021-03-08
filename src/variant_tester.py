from html_file_generator import remove_file
from layout_tester import run_test_using_js_diff_detect, test_combination
from webdrivers import chrome, firefox, safari
from test_subject import TestSubject
from web_page_creation.test_subject_converter import saveTestSubjectAsWebPage
import traceback


def get_variant(webdriver, bug_gone, description, diff_method="Python", forced_slow=False):

    browser_name = webdriver.capabilities['browserName']
    browser_version = "unknown"
    if "browserVersion" in webdriver.capabilities:
        browser_version = webdriver.capabilities['browserVersion']
    elif "version" in webdriver.capabilities:
        browser_version = webdriver.capabilities['version']
    window_size = webdriver.get_window_size()
    return {
        "description": description,
        "bug_detected": not bug_gone,
        "browser": browser_name,
        "browser_version": browser_version,
        "window_size": window_size,
        "diff_method": diff_method,
        "forced_slow": forced_slow,
    }


def print_crash_output(variant_description):
    """
    Print helpful output after crashing
    """
    exception_lines = traceback.format_exc().splitlines()
    nonblank_lines = list(filter(lambda x: x, exception_lines))
    lastline = nonblank_lines[-1] if len(nonblank_lines) > 0 else ""
    print(f"Variant '{variant_description}' Failed: \n  {lastline}")


def test_variants(test_subject: TestSubject):

    variants = []

    # Regular run
    description = "Default Variant"
    chrome_webdriver = chrome.getWebDriver()
    bug_gone, *_ = test_combination(chrome_webdriver, test_subject)
    variants.append(get_variant(chrome_webdriver, bug_gone, description))
    chrome_webdriver.finish()

    # Force a "slow" run
    description = "Slow - Forced Waits"
    chrome_webdriver = chrome.getWebDriver()
    bug_gone, *_ = test_combination(chrome_webdriver, test_subject, slow=True)
    variants.append(get_variant(chrome_webdriver, bug_gone, description, forced_slow=True))
    chrome_webdriver.finish()

    # Smaller Window
    description = "Smaller Window Size"
    chrome_webdriver = chrome.getWebDriver(window_width=500, window_height=500)
    bug_gone, *_ = test_combination(chrome_webdriver, test_subject)
    variants.append(get_variant(chrome_webdriver, bug_gone, description))
    chrome_webdriver.finish()

    # Larger Window Size
    description = "Larger Window Size"
    chrome_webdriver = chrome.getWebDriver(window_width=2400, window_height=2400)
    bug_gone, *_ = test_combination(chrome_webdriver, test_subject)
    variants.append(get_variant(chrome_webdriver, bug_gone, description))
    chrome_webdriver.finish()

    # Using JS Change Detection
    description = "JavaScript Difference Detection"
    chrome_webdriver = chrome.getWebDriver()
    test_filepath, test_web_page = saveTestSubjectAsWebPage(test_subject)
    differences = run_test_using_js_diff_detect(test_web_page, chrome_webdriver, slow=True)
    bug_gone = differences is None
    variants.append(get_variant(chrome_webdriver, bug_gone, description, diff_method="JavaScript"))
    remove_file(test_filepath)
    chrome_webdriver.finish()

    # Run in Firefox
    try:
        description = "Firefox Browser"
        firefox_webdriver = firefox.getWebDriver()
        bug_gone, *_ = test_combination(firefox_webdriver, test_subject)
        variants.append(get_variant(firefox_webdriver, bug_gone, description))
        firefox_webdriver.finish()
    except:
        print_crash_output(description)

    # Run in Safari
    try:
        description = "Safari Browser"
        safari_webdriver = safari.getWebDriver()
        bug_gone, *_ = test_combination(safari_webdriver, test_subject)
        variants.append(get_variant(safari_webdriver, bug_gone, description))
        safari_webdriver.finish()
    except:
        print_crash_output(description)

    # Summarize the variants
    summary = {}
    for variant in variants:
        summary[variant["description"]] = variant["bug_detected"]

    return {
        "Test Variant Summary": summary,
        "Test Variant Details": variants
    }
