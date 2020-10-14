from random import randint
from css_generators.number import generate as generate_number

suffixes = ['cap', 'ch', 'em', 'ex', 'ic', 'lh', 'rem', 'rlh', 'vh', 'vw',
            'vi', 'vb', 'vmin', 'vmax', 'px', 'cm', 'mm', 'Q', 'in', 'pc',
            'pt', 'mozmm', '']


def generate_suffix():
    return suffixes[randint(0, len(suffixes) - 1)]


def generate():
    number = generate_number()
    suffix = generate_suffix()
    return f'{number}{suffix}'
