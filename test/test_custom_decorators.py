import unittest
import os, sys
sys.path.insert(0, "./src")

from css_generators.custom_generators import custom_generators, generator, _list_of_lengths

class TestCustomDecorators(unittest.TestCase):

    def test_generator_decorator(self):
        def example(): return "__test__"
        decorated_example = generator("__style_name__")(example)
        stored_examples = custom_generators.get("__style_name__")
        self.assertEqual(1, len(stored_examples))
        self.assertEqual("__test__", example())
        self.assertEqual("__test__", decorated_example())
        self.assertEqual("__test__", stored_examples[0]())
        self.assertEqual(example, decorated_example)
        self.assertEqual(example, stored_examples[0])
    
    def test__list_of_lengths(self):
        results = [_list_of_lengths() for _ in range(10)]
        self.assertFalse(all([r == results[0] for r in results]))
        self.assertTrue(all([len(r.split()) > 0 for r in results]))


if __name__ == '__main__':
    unittest.main()