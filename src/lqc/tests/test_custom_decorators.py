import unittest

from lqc.generate.css.custom_generators import custom_generators, generator, grid_template_list, generators_for

class TestCustomDecorators(unittest.TestCase):

    def test_generator_decorator(self):
        custom_generators.clear()
        def example(): return "custom_styles"
        decorated_example = generator("_style_name_")(example)
        stored_examples = generators_for("_style_name_")
        self.assertEqual(1, len(stored_examples))
        self.assertEqual("custom_styles", example())
        self.assertEqual("custom_styles", decorated_example())
        self.assertEqual("custom_styles", stored_examples[0]())
        self.assertEqual(example, decorated_example)
        self.assertEqual(example, stored_examples[0])

    def test_generator_decorator_multiple(self):
        custom_generators.clear()
        def example(): return "custom_styles"
        example_copy1 = generator("_style_name_1_")(example)
        example_copy2 = generator("_style_name_2_")(example_copy1)
        self.assertEqual(1, len(generators_for("_style_name_1_")))
        self.assertEqual(1, len(generators_for("_style_name_2_")))
        self.assertEqual(example, example_copy1)
        self.assertEqual(example, example_copy2)
        self.assertEqual("custom_styles", generators_for("_style_name_1_")[0]())
        self.assertEqual("custom_styles", generators_for("_style_name_2_")[0]())
    
    def test_grid_template(self):
        results = [grid_template_list() for _ in range(10)]
        self.assertFalse(all([r == results[0] for r in results]))
        self.assertTrue(all([len(r.split()) > 0 for r in results]))


if __name__ == '__main__':
    unittest.main()