from abc import ABC
from collections.abc import Iterator

from processor import AbstractProcessor
from reader import AbstractReader

class AbstractMeter(Iterator, ABC):
    def __init__(self, name: str, unit: str, sn: str, reader: AbstractReader, processor: AbstractProcessor):
        self.name = name
        self.unit = unit
        self.sn = sn
        self.reader = reader
        self.processor = processor

    def __next__(self) -> float:
        return self.processor.process(next(self.reader))