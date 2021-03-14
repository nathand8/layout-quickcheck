import os, sys

sys.path.insert(0, "./src")

import unittest
from css_generators.style_generator_config import StyleGeneratorConfig
from style_log_generator import generate_style

class TestStringMethods(unittest.TestCase):

    def test_generate_style(self):
        config = {
            "style-weights": {
                "margin-bottom": 0,
                "margin-left": 100,
            }
        }
        StyleGeneratorConfig(config)
        styles = generate_style()
        self.assertFalse("margin-bottom" in styles)
        self.assertTrue("margin-left" in styles)


if __name__ == '__main__':
    unittest.main()