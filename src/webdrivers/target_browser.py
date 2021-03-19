from variants import getTargetBrowserDriver
from selenium.common.exceptions import InvalidSessionIdException

class TargetBrowser():

    def __init__(self):
        self.driver = getTargetBrowserDriver()
    
    def getDriver(self):
        try:
            self.driver.get_window_size()
        except InvalidSessionIdException:
            self.driver.finish()
            self.driver = getTargetBrowserDriver()
        return self.driver