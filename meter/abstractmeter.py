from abc import ABC, abstractmethod
from collections.abc import Iterator

class AbstractMeter(Iterator, ABC):
    def __init__(self, name: str, unit: str, sn: str|None = None):
        self.name = name
        self.unit = unit
        self.sn = sn