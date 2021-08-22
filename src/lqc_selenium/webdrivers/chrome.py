import atexit
import types
from lqc.config.config import Config
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver

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


def getWebDriver(window_width=1000, window_height=1000, headless=True, chrome_args=[]):

    config = Config()
    driver_path = config.getChromeDriverPath()
    if not driver_path:
        raise RuntimeError("Chrome Driver not found")

    chrome_options = ChromeOptions()

    if headless:
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
    if config.getChromeBinaryPath():
        chrome_options.binary_location = config.getChromeBinaryPath()
    
    for arg in chrome_args:
        chrome_options.add_argument(arg)

    chrome_webdriver = WebDriver(executable_path=driver_path, options=chrome_options)
    
    chrome_webdriver.set_window_size(window_width, window_height)

    chrome_webdriver.finish = types.MethodType(finish, chrome_webdriver)
    atexit.register(chrome_webdriver.finish)

    return chrome_webdriver

