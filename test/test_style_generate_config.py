import unittest
from src.config import Config

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
        sgc = Config(config)
        self.assertAlmostEqual(0.00, sgc.getStyleProbability("margin-top"))
        self.assertAlmostEqual(0.00, sgc.getStyleProbability("margin-bottom"))
        self.assertAlmostEqual(1.00, sgc.getStyleProbability("margin-left"))
        self.assertAlmostEqual(1.00, sgc.getStyleProbability("margin-right"))
        self.assertAlmostEqual(0.15, sgc.getStyleProbability("border-left"))
        self.assertAlmostEqual(0.10, sgc.getStyleProbability("border-right"))

    def test_getStyleValueWeights(self):
        config = {
            "style-weights": {
                "max-width:<percent>": -10,
                "max-width:<length>": 20,
                "max-width:auto": 75,
                "max-width:none": 100,
                "max-width:<custom_generator>": 120,
            }
        }
        sgc = Config(config)
        self.assertEqual(0, sgc.getStyleValueWeights("max-width", value_type="percent"))
        self.assertEqual(20, sgc.getStyleValueWeights("max-width", value_type="length"))
        self.assertEqual(75, sgc.getStyleValueWeights("max-width", keyword="auto"))
        self.assertEqual(100, sgc.getStyleValueWeights("max-width", keyword="none"))
        self.assertEqual(120, sgc.getStyleValueWeights("max-width", value_type="custom_generator"))
        self.assertEqual(10, sgc.getStyleValueWeights("max-width", value_type="unknown_type"))
        

if __name__ == '__main__':
    unittest.main()