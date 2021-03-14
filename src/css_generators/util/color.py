from random import choice
from css_generators.util.color_keyword import generate as generate_color_keyword
from css_generators.util.color_rgb import generate as generate_color_rgb

COLOR_GENERATORS = [generate_color_keyword, generate_color_rgb]


def generate():
    gen = choice(COLOR_GENERATORS)
    return gen()
