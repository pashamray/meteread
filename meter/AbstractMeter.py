from abc import ABC
from collections.abc import Iterator

class AbstractMeter(Iterator, ABC):
    def __init__(self, name: str, unit: str, processor: Iterator, sn: str|None = None):
        self.name = name
        self.unit = unit
        self.sn = sn
        self.processor = processor

    def __next__(self) -> float:
        if self.processor:
            return next(self.processor)
        raise StopIteration