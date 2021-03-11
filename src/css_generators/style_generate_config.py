DEFAULT_STYLE_WEIGHT = 10

def _weightToProbability(weight):
    return weight/100

def _bound(low, high, value):
    return max(low, min(high, value))

class StyleGenerateConfig:
    """ Singleton Class """
    __instance = None

    def __new__(cls, config=None):
        """ Singleton Constructor/Accessor 
        If constructed with config, replace the singleton instance
        If called without config, return the existing singleton instance
        """
        if config != None:
            cls.__instance = super(StyleGenerateConfig, cls).__new__(cls)
            # Class Initialization Code
            cls.__instance.style_weights = config.get("style-weights", {})
        elif cls.__instance == None:
            raise RuntimeError("StyleGenerateConfig must be initialized before use")

        return cls.__instance
    
    def getStyleProbability(self, style_name):
        weight = self.style_weights.get(style_name, DEFAULT_STYLE_WEIGHT)
        weight = _bound(0, 100, weight)
        return _weightToProbability(weight)
        
