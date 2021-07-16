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
    return str(random.randint(-200, 200)) + "%"

def _p_percent():
    """ Positive Percentage """
    return str(random.randint(0, 100)) + "%"

def _p_length_fr():
    """ Positive Length in fractional units. Eg 12fr """
    return str(random.randint(0, 100)) + "fr"

def _rand_pick(generators_list):
    """ Pick a random generator from the list and invoke it """
    generator = random.choice(generators_list)
    return generator()

def _p_deg_angle():
    """ Positive degree angle betwee 0 and 360 
        eg. 25deg, 180deg
    """
    return f"{random.randint(0, 360)}deg"

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

@generator("grid-column-start")
@generator("grid-column-end")
@generator("grid-row-start")
@generator("grid-row-end")
def small_number():
    return str(random.randint(-10, 10))

@generator("grid-column-start")
@generator("grid-column-end")
@generator("grid-row-start")
@generator("grid-row-end")
def span_small_positive_number():
    return "span " + str(random.randint(0, 10))

@generator("transform")
def transform_translate():
    value_types = [_p_length_px, _p_percent]
    return f"translate({_rand_pick(value_types)}, {_rand_pick(value_types)})"

@generator("transform")
def transform_matrix():
    coords = [str(random.randint(0, 10)) for x in range(6)]
    return f"matrix({','.join(coords)})"

@generator("transform")
def transform_scale():
    gen = lambda : random.gammavariate(1.2, 2)
    return f"scale({gen()}, {gen()})"

@generator("transform")
def transform_skew():
    return f"skew({_p_deg_angle()}, {_p_deg_angle()})"

@generator("transform")
def transform_rotate():
    return f"rotate({_p_deg_angle()})"