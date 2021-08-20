import unittest

from lqc.config.config import Config
from lqc.generate.style_log_generator import generate_styles

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