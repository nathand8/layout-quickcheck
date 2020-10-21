from random import choice
from css_generators.integer import generate as generate_integer

number_generators = [generate_integer]


def pick_generator():
    return choice(number_generators)


def generate():
    generator = pick_generator()
    return generator()
