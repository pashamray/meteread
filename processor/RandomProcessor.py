import random

from processor.AbstractProcessor import AbstractProcessor

class RandomProcessor(AbstractProcessor):

    def __next__(self) -> float:
        return round(random.random() * 5, 2)