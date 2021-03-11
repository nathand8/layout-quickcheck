import unittest
from src.css_generators.style_generate_config import StyleGenerateConfig

class TestStringMethods(unittest.TestCase):

    def test_getStyleProbability(self):
        config = {
            "style-weights": {
                "margin-top": -10,
                "margin-bottom": 0,
                "margin-left": 200,
                "margin-right": 100,
                "border-left": 15,
                # "border-right": unset
            }
        }
        sgc = StyleGenerateConfig(config)
        self.assertAlmostEqual(0.00, sgc.getStyleProbability("margin-top"))
        self.assertAlmostEqual(0.00, sgc.getStyleProbability("margin-bottom"))
        self.assertAlmostEqual(1.00, sgc.getStyleProbability("margin-left"))
        self.assertAlmostEqual(1.00, sgc.getStyleProbability("margin-right"))
        self.assertAlmostEqual(0.15, sgc.getStyleProbability("border-left"))
        self.assertAlmostEqual(0.10, sgc.getStyleProbability("border-right"))


if __name__ == '__main__':
    unittest.main()