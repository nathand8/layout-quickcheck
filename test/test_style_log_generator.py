import os, sys

sys.path.insert(0, "./src")

import unittest
from config import Config
from style_log_generator import generate_styles

class TestStringMethods(unittest.TestCase):

    def test_generate_style(self):
        config = {
            "style-weights": {
                "margin-bottom": 0,
                "margin-left": 100,
            }
        }
        Config(config)
        styles = generate_styles()
        self.assertFalse("margin-bottom" in styles)
        self.assertTrue("margin-left" in styles)


if __name__ == '__main__':
    unittest.main()