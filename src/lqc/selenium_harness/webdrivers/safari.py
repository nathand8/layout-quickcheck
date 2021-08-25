from lqc.config.config import Config
from selenium.webdriver.safari.webdriver import WebDriver
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


def getWebDriver(window_width=1000, window_height=1000):

    config = Config()
    driver_path = config.getSafariDriverPath()
    if not driver_path:
        raise RuntimeError("Safari Driver not found")

    safari_webdriver = WebDriver(executable_path=driver_path)
    
    safari_webdriver.set_window_size(window_width, window_height)

    safari_webdriver.finish = types.MethodType(finish, safari_webdriver)
    atexit.register(safari_webdriver.finish)

    return safari_webdriver

