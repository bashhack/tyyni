import random
import string


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))
