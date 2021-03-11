
class StyleGenerateConfig():

    def __init__(self, config):
        self.style_weights = config["style_weights"]
    
    def getStyleProbability(self, style_name):
        
