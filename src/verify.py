from layout_tester import run_test_on_page, run_test_using_js_diff_detect
import sys
from webdrivers import chrome
from webdrivers import firefox

if __name__ == "__main__":

    url = sys.argv[1]

    chrome_webdriver = chrome.getWebDriver()

    browser_version = chrome_webdriver.capabilities['browserVersion']
    driver_version = chrome_webdriver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    window_size = chrome_webdriver.get_window_size()
    print("\nChrome Version   :", browser_version)
    print("WebDriver Version:", driver_version)
    print("Window Size:", window_size)

    # Using the same method that was used for original bug detection
    differences = run_test_on_page(url, chrome_webdriver, slow=True)
    print("\nChrome: Using regular difference detection...")
    print("Differences:", differences)

    # Using the JS difference detection method
    differences = run_test_using_js_diff_detect(url, chrome_webdriver, slow=True)
    print("\nChrome: Using js difference detection...")
    print("Differences:", differences)



    firefox_webdriver = firefox.getWebDriver()

    browser_version = firefox_webdriver.capabilities['browserVersion']
    driver_version = firefox_webdriver.capabilities
    window_size = firefox_webdriver.get_window_size()
    print("\nFirefox Version   :", browser_version)
    print("WebDriver Version:", driver_version)
    print("Window Size:", window_size)


    browser = firefox_webdriver.capabilities["browserName"]

    # Using the same method that was used for original bug detection
    differences = run_test_on_page(url, firefox_webdriver, slow=True)
    print("\nFirefox: Using regular difference detection...")
    print("Differences:", differences)

    # Using the JS difference detection method
    differences = run_test_using_js_diff_detect(url, firefox_webdriver, slow=True)
    print("\nFirefox: Using js difference detection...")
    print("Differences:", differences)