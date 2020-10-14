from random import randint
from css_generators.integer import generate as generate_integer

number_generators = [generate_integer]


def pick_generator():
    return number_generators[randint(0, len(number_generators) - 1)]


def generate():
    generator = pick_generator()
    return generator()
