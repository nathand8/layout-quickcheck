from random import choice, randint

MAX_NUMBER = 2000

prefixes = ["", "+", "-"]


def generate_prefix():
    return choice(prefixes)


def generate():
    prefix = generate_prefix()
    number = randint(0, MAX_NUMBER)
    return f"{prefix}{number}"
