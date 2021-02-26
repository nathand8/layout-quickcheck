import os
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


def getWebDriver(window_width=1000, window_height=1000):

    driver_path = os.environ.get("SAFARI_DRIVER_PATH", None)
    if not driver_path:
        raise RuntimeError("Safari Driver not found")

    safari_webdriver = WebDriver(executable_path=driver_path)
    
    safari_webdriver.set_window_size(window_width, window_height)

    safari_webdriver.finish = types.MethodType(finish, safari_webdriver)
    atexit.register(lambda: safari_webdriver.finish())

    return safari_webdriver

