import random

from reader.AbstractReader import AbstractReader

class RandomReader(AbstractReader):

    def __next__(self):
        return round(random.random() * 5, 2)