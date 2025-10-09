from collections.abc import Iterator
from time import sleep

from processor.AbstractProcessor import AbstractProcessor

class DelayProcessor(AbstractProcessor):
    def __init__(self, processor: Iterator, delay: float = 1.0):
        self.processor = processor
        self.delay = delay

    def __next__(self) -> float:
        sleep(self.delay)
        return next(self.processor)