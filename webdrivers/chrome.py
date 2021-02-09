import os
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import atexit
import types


def finish(webdriver):
    try:
        webdriver.close()
    except:
        pass
    try:
        webdriver.quit()
    except:
        pass


def getWebDriver(window_width=1000, window_height=1000, headless=True):
    global registered, webdrivers_to_close

    chrome_options = ChromeOptions()

    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_webdriver = WebDriver(
        executable_path=os.environ.get("CHROME_DRIVER_PATH"), options=chrome_options
    )
    chrome_webdriver.set_window_size(window_width, window_height)

    chrome_webdriver.finish = types.MethodType(finish, chrome_webdriver)
    atexit.register(lambda: chrome_webdriver.finish())

    return chrome_webdriver

