from abc import ABC, abstractmethod
from collections.abc import Iterator


class AbstractProcessor(Iterator, ABC):
    @abstractmethod
    def __next__(self) -> float:
        raise StopIteration