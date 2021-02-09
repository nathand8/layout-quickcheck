import os
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import atexit

webdrivers_to_close = []
registered = False


def terminate_browsers():
    global webdrivers_to_close

    print("Closing Firefox WebDrivers")
    for webdriver in webdrivers_to_close:
        try:
            webdriver.close()
        except:
            pass


def getWebDriver(window_width=1000, window_height=1000, headless=True):
    global registered, webdrivers_to_close

    firefox_options = FirefoxOptions()

    if headless:
        firefox_options.add_argument("--headless")
        # firefox_options.add_argument('--no-sandbox')
        # firefox_options.add_argument('--disable-dev-shm-usage')

    firefox_webdriver = WebDriver(
        executable_path=os.environ.get("FIREFOX_DRIVER_PATH"), 
        options=firefox_options
    )

    firefox_webdriver.set_window_size(window_width, window_height)

    webdrivers_to_close.append(firefox_webdriver)

    if not registered:
        atexit.register(terminate_browsers)
        registered = True

    return firefox_webdriver

