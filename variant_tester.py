from layout_tester import test_combination
from webdrivers import chrome
from test_subject import TestSubject



def get_variant(webdriver, bug_gone, description):
    browser_version = webdriver.capabilities['browserVersion']
    driver_version = webdriver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    window_size = webdriver.get_window_size()
    return {
        "description": description,
        "bug_detected": not bug_gone,
        "browser": "Chrome",
        "browser_version": browser_version,
        "browser_driver_version": driver_version,
        "window_size": window_size,
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

    return variants
