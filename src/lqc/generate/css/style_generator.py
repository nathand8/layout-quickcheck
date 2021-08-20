import random
from lqc.config.config import Config
from lqc.generate.css import custom_generators
from lqc.generate.css.util.length import generate as generate_length

class StyleGenerator():

    def __init__(self):
        self.config = Config()

    def _lengthGenerator(self, style_name):
        generator = generate_length
        weight = self.config.getStyleValueWeights(style_name, value_type="length")
        return generator, weight
    
    def _percentageGenerator(self, style_name):
        generator = custom_generators._percent
        weight = self.config.getStyleValueWeights(style_name, value_type="percentage")
        return generator, weight

    def _keywordGenerators(self, style_name, keywords):
        return [(lambda x=k: x, self.config.getStyleValueWeights(style_name, keyword=k)) for k in keywords]

    def _customGenerators(self, style_name):
        generators = custom_generators.generators_for(style_name)
        return [(generator, self.config.getStyleValueWeights(style_name, value_type=generator.__name__)) for generator in generators]

    def getWeightedGenerators(self, style_meta_data):
        """ Get a list of possible generators with weights """
        ret = []
        style_name = style_meta_data["name"]
        if "typedom_types" in style_meta_data:
            if "Length" in style_meta_data["typedom_types"]:
                ret.append(self._lengthGenerator(style_name))
            if "Percentage" in style_meta_data["typedom_types"]:
                ret.append(self._percentageGenerator(style_name))
            if "Keyword" in style_meta_data["typedom_types"] and "keywords" in style_meta_data:
                ret.extend(self._keywordGenerators(style_name, style_meta_data["keywords"]))
        ret.extend(self._customGenerators(style_name))
        return ret
    
    def pickGenerator(self, style_meta_data):
        """ Pick a generator at random, honoring weights """
        weighted_generators = self.getWeightedGenerators(style_meta_data)
        if len(weighted_generators) > 0:
            generators = [x[0] for x in weighted_generators]
            weights = [x[1] for x in weighted_generators]
            return random.choices(generators, weights)[0]
        else:
            return None
