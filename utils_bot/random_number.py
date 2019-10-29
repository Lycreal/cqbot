import random


def square_random(start: float, end: float):
    r = random.random() ** 2
    return start + (end - start) * r
