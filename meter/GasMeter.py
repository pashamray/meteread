from meter import AbstractMeter
from processor import AbstractProcessor
from reader import AbstractReader

class GasMeter(AbstractMeter):
    def __init__(self, name: str, reader: AbstractReader, processor: AbstractProcessor):
        super().__init__(
            name=name,
            reader=reader,
            processor=processor,
        )
