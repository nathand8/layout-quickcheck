from layout_tester import run_test_on_page, run_test_using_js_diff_detect
import sys
from webdrivers import chrome

if __name__ == "__main__":

    chrome_webdriver = chrome.getWebDriver()

    browser_version = chrome_webdriver.capabilities['browserVersion']
    driver_version = chrome_webdriver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    window_size = chrome_webdriver.get_window_size()
    print("Chrome Version   :", browser_version)
    print("WebDriver Version:", driver_version)
    print("Window Size:", window_size)

    url = sys.argv[1]

    # Using the same method that was used for original bug detection
    differences = run_test_on_page(url, chrome_webdriver, slow=True)
    print("\nUsing regular difference detection...")
    print("Differences:", differences)

    # Using the JS difference detection method
    differences = run_test_using_js_diff_detect(url, chrome_webdriver, slow=True)
    print("\nUsing js difference detection...")
    print("Differences:", differences)
