from collections.abc import Iterator
from time import sleep

from reader.AbstractReader import AbstractReader

class DelayReader(AbstractReader):
    def __init__(self, reader: AbstractReader, delay: float = 1.0):
        self.reader = reader
        self.delay = delay

    def __next__(self):
        sleep(self.delay)
        return next(self.reader)