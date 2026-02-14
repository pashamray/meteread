from abc import abstractmethod, ABC
from typing import Any, Generator


class AbstractProcessor(ABC):
    def __init__(self, sn: str, unit: str):
        self.sn = sn
        self.unit = unit

    @abstractmethod
    def __call__(self, data) -> Generator[dict[str, str | None], Any, None]:
        pass