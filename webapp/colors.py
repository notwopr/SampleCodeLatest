import random


class ColorGenerator:
    def gen_random_hex(self):
        return "#{:06x}".format(random.randrange(256 ** 3))
