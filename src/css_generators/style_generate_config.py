DEFAULT_STYLE_WEIGHT = 10

def _weightToProbability(weight):
    return weight/100

def _bound(low, high, value):
    return max(low, min(high, value))

class StyleGenerateConfig():
    """ Singleton Config """
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if StyleGenerateConfig.__instance == None:
            raise RuntimeError("StyleGenerateConfig accessed before initialization")
        return StyleGenerateConfig.__instance

    def __init__(self, config):
        """ Virtually private constructor. """
        if StyleGenerateConfig.__instance != None:
            raise RuntimeError("StyleGenerateConfig is a Singleton, the constructor may only be called once.")
        else:
            StyleGenerateConfig.__instance = self

        self.style_weights = config.get("style-weights", {})
    
    def getStyleProbability(self, style_name):
        weight = self.style_weights.get(style_name, DEFAULT_STYLE_WEIGHT)
        weight = _bound(0, 100, weight)
        return _weightToProbability(weight)
        
