from processor.AbstractProcessor import AbstractProcessor

class ZeroProcessor(AbstractProcessor):

    def __next__(self) -> float:
        return 0.0