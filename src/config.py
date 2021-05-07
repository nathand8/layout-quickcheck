DEFAULT_STYLE_WEIGHT = 10
DEFAULT_STYLE_VALUE_WEIGHT = 10

def _weightToProbability(weight):
    return weight/100

def _bound(low, high, value):
    return max(low, min(high, value))

class Config:
    """ Singleton Class """
    __instance = None

    def __new__(cls, config=None):
        """ Singleton Constructor/Accessor 
        If constructed with config, replace the singleton instance
        If called without config, return the existing singleton instance
        """
        if config != None:
            cls.__instance = super(Config, cls).__new__(cls)
            # Class Initialization Code
            cls.__instance.style_weights = config.get("style-weights", {})
            cls.__instance.target_browser_variant = config.get("target-browser-variant", None)
            paths = config.get("paths", {})
            cls.__instance.path_bug_reports_dir = paths.get("bug-reports-directory", "./bug_reports")
            cls.__instance.path_tmp_files_dir = paths.get("tmp-files-directory", "./tmp_generated_files")

        elif cls.__instance == None:
            raise RuntimeError("Config must be initialized before use")

        return cls.__instance
    
    def getStyleProbability(self, style_name):
        weight = self.style_weights.get(style_name, DEFAULT_STYLE_WEIGHT)
        weight = _bound(0, 100, weight)
        return _weightToProbability(weight)
    
    def getStyleValueWeights(self, style_name, value_type="", keyword=None):
        key_suffix = keyword if keyword != None else "<" + value_type + ">"
        style_and_type = style_name + ":" + key_suffix
        weight = self.style_weights.get(style_and_type, DEFAULT_STYLE_VALUE_WEIGHT)
        return _bound(0, 100000, weight)
    
    def getTargetBrowserVariant(self):
        return self.target_browser_variant

    def getBugReportDirectory(self):
        return self.path_bug_reports_dir

    def getTmpFilesDirectory(self):
        return self.path_tmp_files_dir
    