from abc import abstractmethod, ABC


class AbstractProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass