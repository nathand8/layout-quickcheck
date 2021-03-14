import unittest
import os, sys

sys.path.insert(0, "./src")

from css_generators.style_generator import StyleGenerator
from css_generators.style_generator_config import StyleGeneratorConfig
from css_generators.custom_generators import custom_generators

class TestCustomDecorators(unittest.TestCase):

    def test__length_generator(self):
        StyleGeneratorConfig({"style-weights": {"margin-top:<length>": 20}})
        sg = StyleGenerator()
        g, w = sg._lengthGenerator("margin-top")
        self.assertFalse(g().isalpha())
        self.assertFalse(g().isdigit())
        self.assertEqual(20, w)

        _, w = sg._lengthGenerator("padding-right")
        self.assertEqual(10, w)

    def test__percentage_generator(self):
        StyleGeneratorConfig({"style-weights": {"width:<percentage>": 20}})
        sg = StyleGenerator()
        g, w = sg._percentageGenerator("width")
        self.assertTrue(g().endswith("%"))
        self.assertEqual(20, w)

        _, w = sg._percentageGenerator("height")
        self.assertEqual(10, w)

    def test__keyword_generators(self):
        StyleGeneratorConfig({"style-weights": {"display:inline": 20}})
        sg = StyleGenerator()
        l = sg._keywordGenerators("display", ["inline", "block", "grid", "table"])
        self.assertEqual(len(l), 4)
        for g, w in l:
            if g() == "inline":
                self.assertEqual(20, w)
            else:
                self.assertEqual(10, w)

    def test__custom_generators(self):
        StyleGeneratorConfig({"style-weights": {"width:<custom_percentage_generator>": 20}})
        sg = StyleGenerator()
        def custom_percentage_generator(): return "10%"
        def custom_length_generator(): return "50px"
        custom_generators["width"] = [custom_percentage_generator, custom_length_generator]
        l = sg._customGenerators("width")
        self.assertEqual(len(l), 2)
        for g, w in l:
            if g() == "10%":
                self.assertEqual(20, w)
            else:
                self.assertEqual(10, w)
    
    def test_getWeightedGenerators(self):
        StyleGeneratorConfig({"style-weights": {
                "max-width:always": 30,
                "max-width:<length>": 50,
                "max-width:<percentage>": 70,
                "max-width:<custom_percentage_generator>": 90,
            }})
        sg = StyleGenerator()
        def custom_percentage_generator(): return "10_custom_%"
        def custom_length_generator(): return "50_custom_px"
        custom_generators["max-width"] = [custom_percentage_generator, custom_length_generator]
        style_meta_data = {
            "name": "max-width",
            "keywords": ["none", "always"],
            "typedom_types": ["Keyword", "Length", "Percentage"],
        }
        l = sg.getWeightedGenerators(style_meta_data)
        self.assertEqual(len(l), 6)
        all_values = [g() for g, w in l]
        self.assertTrue("10_custom_%" in all_values)
        self.assertTrue("50_custom_px" in all_values)
        self.assertTrue("none" in all_values)
        self.assertTrue("always" in all_values)
        for g, w in l:
            if g() == "10_custom_%":
                self.assertEqual(w, 90)
            elif g() == "50_custom_px":
                self.assertEqual(w, 10)
            elif g() == "none":
                self.assertEqual(w, 10)
            elif g() == "always":
                self.assertEqual(w, 30)
            elif "%" in g():
                self.assertEqual(w, 70)
            else:
                self.assertEqual(w, 50)

    def test_getWeightedGenerators_minimal(self):
        style_meta_data = {
            "name": "min-width",
            "typedom_types": ["Percentage"],
        }
        sg = StyleGenerator()
        l = sg.getWeightedGenerators(style_meta_data)
        self.assertEqual(len(l), 1)
        self.assertTrue("%" in l[0][0]())
        self.assertEqual(10, l[0][1])
        



if __name__ == '__main__':
    unittest.main()