from lqc.config.config import Config
from lqc_selenium.webdrivers import chrome, firefox, safari

cached_variants = None
target_variant = None

def getVariants():
    global cached_variants, target_variant
    if cached_variants is not None:
        return cached_variants

    conf = Config()
    variants = conf.getVariants()
    out = []
    for variant in variants:
        cls = {
            "chrome": ChromeVariant,
            "firefox": FirefoxVariant,
            "safari": SafariVariant,
        }.get(variant.get("type"))
        if not cls:
            print(f"Warning: Unknown variant type {variant!r}")
        kwargs = variant.copy()
        if "type" in kwargs: del kwargs["type"]
        if "target" in kwargs: del kwargs["target"]
        try:
            v = cls(**kwargs)
        except RuntimeError as e:
            print(f"Error in variant {variant!r}:\n  {cls.__name}: {e}")
        else:
            out.append(v)
            if "target" in kwargs and kwargs["target"]:
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

class ChromeVariant:
    def __init__(self, name=None, slow=False, width=None, height=None, args=None):
        self.kwargs = {}
        if width:
            self.kwargs["window_width"] = width
        if height:
            self.kwargs["window_height"] = width
        if args:
            self.kwargs["chrome_args"] = args

        self.force_slow = slow
        self.name = name or "Chrome(slow={}, width={}, height={}, args={})".format(slow, width, height, args)

    def webdriver(self):
        return chrome.getWebDriver(**self.kwargs)

class FirefoxVariant:
    def __init__(self, name=None, slow=False, options=None):
        self.kwargs = {}
        if options:
            self.kwargs["options_args"] = options
        self.force_slow = slow
        self.name = name or "Firefox(slow={}, options={})".format(slow, options)

    def webdriver(self):
        return firefox.getWebDriver(**self.kwargs)

class SafariVariant:
    def __init__(self, name=None, slow=False):
        self.force_slow = slow
        self.name = name or "Safari(slow={})".format(slow)
        self.kwargs = {}

    def webdriver(self):
        return safari.getWebDriver(**self.kwargs)
