import atexit
import types
import subprocess

from lqc.config.config import Config
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver
from selenium.common.exceptions import InvalidSessionIdException

cached_variants = None
target_variant = None

def getVariants():
    global cached_variants, target_variant
    if cached_variants is not None:
        return cached_variants

    conf = Config()
    variants = conf.getVariants()
    out = []
    is_target = False
    for variant in variants:
        is_target = False
        cls = {
            "chrome": ChromeVariant,
            "firefox": FirefoxVariant,
            "safari": SafariVariant,
        }.get(variant.get("type"))
        if not cls:
            print(f"Warning: Unknown variant type {variant!r}")
        kwargs = variant.copy()
        if "type" in kwargs: del kwargs["type"]
        if "target" in kwargs: 
            is_target = kwargs["target"]
            del kwargs["target"]
        try:
            v = cls(**kwargs)
        except RuntimeError as e:
            print(f"Error in variant {variant!r}:\n  {cls.__name}: {e}")
        else:
            out.append(v)
            if is_target:
                if target_variant:
                    print(f"Warning: two variants marked as target variant (ignoring second)")
                else:
                    target_variant = v

    if not target_variant and out:
        target_variant = out[0]
    cached_variants = out
    return cached_variants

def getTargetVariant():
    global target_variant
    getVariants()
    if target_variant:
        return target_variant
    else:
        raise RuntimeError("No variants described in config file!")

def getTargetBrowserDriver():
    return getTargetVariant().webdriver()

def finish(webdriver):
    "Helper method to ensure all webdrivers are closed at finish"
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


def detectDriverPath(driver, config_name):
    status, driver_path = subprocess.getstatusoutput(f"which {driver}")
    if status == 0:
        print(f"Log: No {config_name} path in config. Using {driver_path}")
        return driver_path
    else:
        print(f"Warning: No {config_name} Found. You may need to install {driver} or put the path in the config.")
        return None
    

class Variant:
    def __init__(self, name=None, slow=False):
        self.force_slow = slow
        self.name = name

    def __str__(self):
        return self.name or repr(self)

    def __repr__(self):
        return "Variant()"

    def webdriver(self):
        raise NotImplemented("Variant().webdriver() should be overridden")

class ChromeVariant(Variant):
    def __init__(self, name=None, slow=False, width=1000, height=1000, args=[], headless=True, webdriver_path=None, binary_path=None):
        super().__init__(name, slow)
        self.width = width
        self.height = height
        self.args = args
        self.headless = headless
        self.webdriver_path = webdriver_path or detectDriverPath("chromedriver", "Chrome webdriver_path")
        self.binary_path = binary_path

    def __repr__(self):
        return "Chrome(headless={}, slow={}, width={}, height={}, args={})".format(self.headless, self.force_slow, self.width, self.height, self.args)

    def webdriver(self):
        if not self.webdriver_path:
            raise RuntimeError("Chrome Driver not found")

        chrome_options = ChromeOptions()

        if self.headless:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        if self.binary_path:
            chrome_options.binary_location = self.binary_path
        
        for arg in self.args:
            chrome_options.add_argument(arg)

        chrome_webdriver = ChromeWebDriver(executable_path=self.webdriver_path, options=chrome_options)
        
        chrome_webdriver.set_window_size(self.width, self.height)

        chrome_webdriver.finish = types.MethodType(finish, chrome_webdriver)
        atexit.register(chrome_webdriver.finish)

        return chrome_webdriver

class FirefoxVariant(Variant):
    def __init__(self, name=None, slow=False, width=1000, height=1000, options=None, headless=True, webdriver_path=None, binary_path=None):
        super().__init__(name, slow)
        self.options = options
        self.width = width
        self.height = height
        self.headless = headless
        self.webdriver_path = webdriver_path or detectDriverPath("geckodriver", "Firefox webdriver_path")
        self.binary_path = binary_path

    def __repr__(self):
        return "Firefox(headless={}, slow={}, width={}, height={}, options={})".format(self.headless, self.force_slow, self.width, self.height, self.options)

    def webdriver(self):
        if not self.webdriver_path:
            raise RuntimeError("Firefox Driver not found")

        firefox_options = FirefoxOptions()

        if self.headless:
            firefox_options.add_argument("--headless")
        if self.binary_path:
            firefox_options.binary_location = self.binary_path

        if self.options:
            for property, value in self.options.items():
                firefox_options.set_preference(property, value)

        firefox_webdriver = FirefoxWebDriver(executable_path=self.webdriver_path, options=firefox_options)

        firefox_webdriver.set_window_size(self.width, self.height)

        firefox_webdriver.finish = types.MethodType(finish, firefox_webdriver)
        atexit.register(firefox_webdriver.finish)

        return firefox_webdriver

class SafariVariant(Variant):
    def __init__(self, name=None, width=1000, height=1000, slow=False, webdriver_path=None, binary_path=None):
        super().__init__(name, slow)
        self.width = width
        self.height = height
        self.webdriver_path = webdriver_path or detectDriverPath("safaridriver", "Savari webdriver_path")

    def __repr__(self):
        return "Safari(slow={}, width={}, height={})".format(self.force_slow, self.width, self.height)

    def webdriver(self):
        if not self.webdriver_path:
            raise RuntimeError("Safari Driver not found")

        safari_webdriver = SafariWebDriver(executable_path=self.webdriver_path)
        
        safari_webdriver.set_window_size(self.width, self.height)

        safari_webdriver.finish = types.MethodType(finish, safari_webdriver)
        atexit.register(safari_webdriver.finish)

        return safari_webdriver


class TargetBrowser():
    """
    Helper class that checks the Selenium driver state before returning the driver.
    """

    def __init__(self):
        self.driver = getTargetBrowserDriver()
    
    def getDriver(self):
        try:
            # Checking window size will throw an error if the driver is in a bad state
            self.driver.get_window_size()
        except InvalidSessionIdException:
            self.driver.finish()
            self.driver = getTargetBrowserDriver()
        return self.driver