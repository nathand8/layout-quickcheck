from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from layout_tester import run_test_on_page
import os
import sys

if __name__ == "__main__":

    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_webdriver = WebDriver(
        executable_path=os.environ.get("CHROME_DRIVER_PATH"), options=chrome_options
    )

    # chrome_webdriver.set_window_size(1000, 1000)

    browser_version = chrome_webdriver.capabilities['browserVersion']
    driver_version = chrome_webdriver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    print("Chrome Version   :", browser_version)
    print("WebDriver Version:", driver_version)

    url = sys.argv[1]

    differences = run_test_on_page(url, chrome_webdriver)

    print("Differences:", differences)
