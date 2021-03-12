import random

custom_generators = {}

def generator(style_name):

    def decorator_generator(func):
        custom_generators.setdefault(style_name, [])
        custom_generators[style_name].append(func)
        return func
    
    return decorator_generator


def _length_px():
    """
    Generate a length in px

    Examples:
        12px
        1440px
    """
    MAX_NUMBER = 2000
    i = random.randint(0, MAX_NUMBER)
    return str(i) + "px"


@generator("grid-template-columns")
def _list_of_lengths():
    """
    An arbitrary length list of lengths.

    0 < List Length < ~30 
    List Length = ~3 on average

    Examples:
        grid-template-columns: 1093px, 255px, 1825px, 12px;
        grid-template-columns: 492px;
    """
    l = [_length_px()]
    while random.random() < 0.6:
        l.append(_length_px())
    return " ".join(l)