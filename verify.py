from layout_tester import run_test_on_page
import os
import sys
from webdrivers import chrome

if __name__ == "__main__":

    chrome_webdriver = chrome.getWebDriver()

    browser_version = chrome_webdriver.capabilities['browserVersion']
    driver_version = chrome_webdriver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print("Chrome Version   :", browser_version)
    print("WebDriver Version:", driver_version)

    url = sys.argv[1]

    differences = run_test_on_page(url, chrome_webdriver)

    print("Differences:", differences)
