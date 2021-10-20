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
    def __init__(self, name=None, slow=False, width=None, height=None, args=None):
        super().__init__(name, slow)
        self.width = width
        self.height = height
        self.args = args

    def __repr__(self):
        return "Chrome(slow={}, width={}, height={}, args={})".format(self.force_slow, self.width, self.height, self.args)

    def webdriver(self):
        kwargs = {}
        if width:
            kwargs["window_width"] = self.width
        if height:
            kwargs["window_height"] = self.height
        if args:
            kwargs["chrome_args"] = self.args
        return chrome.getWebDriver(**kwargs)

class FirefoxVariant(Variant):
    def __init__(self, name=None, slow=False, options=None):
        super().__init__(name, slow)
        self.options = options

    def __repr__(self):
        return "Firefox(slow={}, options={})".format(self.force_slow, self.options)

    def webdriver(self):
        kwargs = {}
        if self.options:
            kwargs["options_args"] = self.options
        return firefox.getWebDriver(**kwargs)

class SafariVariant(Variant):
    def __init__(self, name=None, slow=False):
        super().__init__(name, slow)

    def __repr__(self):
        return "Safari(slow={})".format(self.force_slow)

    def webdriver(self):
        kwargs = {}
        return safari.getWebDriver(**kwargs)
