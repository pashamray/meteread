from abc import abstractmethod, ABC


class AbstractProcessor(ABC):
    @abstractmethod
    def __call__(self, data) -> None:
        pass