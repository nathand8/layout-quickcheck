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

# =============================
# Helper Functions
# =============================

def _p_length_px():
    """ Positive Length in pixels. Eg 110px """
    return str(random.randint(0, 2000)) + "px"

def _percent():
    """ Percentage """
    return str(random.randint(0, 100)) + "%"

def _p_length_fr():
    """ Positive Length in fractional units. Eg 12fr """
    return str(random.randint(0, 100)) + "fr"


# =============================
# Custom Generators
# =============================

@generator("grid-template-columns")
@generator("grid-template-rows")
def grid_template_list():
    """
    List of lengths. Values can be a length, percentage, factor, etc

    Examples:
        grid-template-columns: 1093px 255px 1825px 12px 400px;
        grid-template-columns: 1093px 10% 3fr;
    """
    value_types = [_p_length_px, _percent, _p_length_fr]
    list_length = math.ceil(random.gammavariate(2, 2))
    l = [random.choice(value_types)() for _ in range(list_length)]
    return " ".join(l)