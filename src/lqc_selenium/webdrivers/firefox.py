from lqc.config.config import Config
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
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
    try:
        atexit.unregister(webdriver.finish)
    except:
        pass


def getWebDriver(window_width=1000, window_height=1000, headless=True, options_args={}):

    config = Config()
    driver_path = config.getFirefoxDriverPath()
    if not driver_path:
        raise RuntimeError("Firefox Driver not found")

    firefox_options = FirefoxOptions()

    if headless:
        firefox_options.add_argument("--headless")
    if config.getFirefoxBinaryPath():
        firefox_options.binary_location = config.getFirefoxBinaryPath()

    for property, value in options_args.items():
        firefox_options.set_preference(property, value)

    firefox_webdriver = WebDriver(executable_path=driver_path, options=firefox_options)

    firefox_webdriver.set_window_size(window_width, window_height)

    firefox_webdriver.finish = types.MethodType(finish, firefox_webdriver)
    atexit.register(firefox_webdriver.finish)

    return firefox_webdriver

