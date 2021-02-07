import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import atexit


def getWebDriver():
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_webdriver = WebDriver(
        executable_path=os.environ.get("CHROME_DRIVER_PATH"), options=chrome_options
    )
    chrome_webdriver.set_window_size(1000, 1000)

    def terminate_browsers():
        print("closing browsers")
        if chrome_webdriver is not None:
            print("Closing Chrome")
            chrome_webdriver.close()

    atexit.register(terminate_browsers)

    return chrome_webdriver
