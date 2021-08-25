from random import choice


def create_generator(keywords):
    def generate():
        return choice(keywords)

    return generate
