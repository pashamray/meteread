import random

from processor.AbstractProcessor import AbstractProcessor

class RandomProcessor(AbstractProcessor):

    def __next__(self):
        return round(random.random() * 5, 2)