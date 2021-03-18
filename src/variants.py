from webdrivers import chrome, firefox, safari

variants = []
target_variant_generator = None


def variant(name=None, force_slow=False, js_change_detection=False):
    """Decorator - used to specify variants of webdrivers"""

    def decorator_generator(func):
        n = func.__doc__ or func.__name__
        if name is not None:
            n = name
        v = {
            "name": n,
            "driver": func,
            "force_slow": force_slow,
            "js_change_detection": js_change_detection
        }
        variants.append(v)
        return func
    
    return decorator_generator


def getVariants():
    return variants


def target():
    """Decorator - used to specify the webdriver focus on testing"""
    if target_variant_generator:
        raise RuntimeError("Only one @target() browser driver is allowed")

    def decorator_generator(func):
        global target_variant_generator
        target_variant_generator = func
        return func
    
    return decorator_generator


def getTargetBrowserDriver():
    global target_variant_generator
    if not target_variant_generator:
        return variants[0]["driver"]()
    else:
        return target_variant_generator()



# =============================
# Webdriver Variants
# =============================

@variant()
def vanilla_chrome():
    "Chrome - Vanilla"
    return chrome.getWebDriver()

@variant(force_slow=True)
def chrome_force_slow():
    "Chrome - Forced Waits"
    return chrome.getWebDriver()

@variant()
def chrome_smaller_window():
    "Chrome - Smaller Window"
    return chrome.getWebDriver(window_width=500, window_height=500)

@variant()
def chrome_larger_window():
    "Chrome - Larger Window"
    return chrome.getWebDriver(window_width=2400, window_height=2400)

@variant(js_change_detection=True, force_slow=True)
def chrome_js_change_detection():
    "Chrome - Difference detection using JavaScript"
    return chrome.getWebDriver()

@target()
@variant()
def chrome_blink_layout_grid():
    "Chrome --enable-blink-features=LayoutNGGrid"
    return chrome.getWebDriver(chrome_args=["--enable-blink-features=LayoutNGGrid"])

@variant()
def chrome_blink_layout_table():
    "Chrome --enable-blink-features=LayoutNGTable"
    return chrome.getWebDriver(chrome_args=["--enable-blink-features=LayoutNGTable"])

@variant()
def firefox_vanilla():
    "Firefox - Vanilla"
    return firefox.getWebDriver()

@variant()
def safari_vanilla():
    "Safari - Vanilla"
    return safari.getWebDriver()
