from random import choice, random, randint, uniform

# RRGGBB[AA]
# RGB[A]
# rgb[a](R, G, B[, A])
# rgb[a](R G B[ A])

ALPHA_PROB = 0.25


def large_hex_value():
    return "{:02X}".format(randint(0, 255))


def generate_large_hex():
    alpha = large_hex_value() if random() <= ALPHA_PROB else ""
    return f"#{large_hex_value()}{large_hex_value()}{large_hex_value()}{alpha}"


def small_hex_value():
    return "{:01X}".format(randint(0, 15))


def generate_small_hex():
    alpha = small_hex_value() if random() <= ALPHA_PROB else ""
    return f"#{small_hex_value()}{small_hex_value()}{small_hex_value()}{alpha}"


def rgb_int_value():
    return randint(0, 255)


def generate_css3_rgb():
    show_alpha = random() <= ALPHA_PROB
    alpha_prefix = "a" if show_alpha else ""
    alpha_value = f"{uniform(0, 1)}" if random() < 0.5 else f"{randint(0, 100)}%"
    alpha_string = f", {alpha_value}" if show_alpha else ""
    return (
        f"rgb{alpha_prefix}({rgb_int_value()}, {rgb_int_value()}, "
        f"{rgb_int_value()}{alpha_string})"
    )


def generate_css4_rgb():
    show_alpha = random() <= ALPHA_PROB
    alpha_prefix = "a" if show_alpha else ""
    alpha_value = f"{uniform(0, 1)}" if random() < 0.5 else f"{randint(0, 100)}%"
    alpha_string = f" / {alpha_value}" if show_alpha else ""
    return (
        f"rgb{alpha_prefix}({rgb_int_value()} {rgb_int_value()} "
        f"{rgb_int_value()}{alpha_string})"
    )


COLOR_GENERATORS = [
    generate_large_hex,
    generate_small_hex,
    generate_css3_rgb,
    generate_css4_rgb,
]


def generate():
    gen = choice(COLOR_GENERATORS)
    return gen()
