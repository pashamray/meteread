from abc import ABC
from collections.abc import Iterator

from reader.AbstractReader import AbstractReader

class AbstractMeter(Iterator, ABC):
    def __init__(self, name: str, unit: str, sn: str, reader: AbstractReader):
        self.name = name
        self.unit = unit
        self.sn = sn
        self.reader = reader

    def __next__(self) -> float:
        if self.reader:
            return next(self.reader)
        raise StopIteration