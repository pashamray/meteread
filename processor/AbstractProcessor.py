from abc import abstractmethod, ABC


class AbstractProcessor(ABC):
    def __init__(self, sn: str = 'None', unit: str = 'None'):
        self.sn = sn
        self.unit = unit

    @abstractmethod
    def __call__(self, data) -> None:
        pass