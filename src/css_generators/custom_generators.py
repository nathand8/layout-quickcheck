import random, math

custom_generators = {}

def generator(style_name):

    def decorator_generator(func):
        custom_generators.setdefault(style_name, [])
        custom_generators[style_name].append(func)
        return func
    
    return decorator_generator

def generators_for(style_name):
    return custom_generators.get(style_name, [])


def _length_px():
    """
    Generate a length in px

    Example:
        1440px
    """
    MAX_NUMBER = 2000
    i = random.randint(0, MAX_NUMBER)
    return str(i) + "px"


@generator("grid-template-columns")
def _list_of_lengths():
    """
    An arbitrary length list of lengths.

    Examples:
        grid-template-columns: 1093px 255px 1825px 12px;
        grid-template-columns: 492px;
    """
    list_length = math.ceil(random.gammavariate(2, 2))
    l = [_length_px() for _ in range(list_length)]
    return " ".join(l)