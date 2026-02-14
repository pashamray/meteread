from meter import AbstractMeter
from processor import AbstractProcessor
from reader import AbstractReader

class WaterMeter(AbstractMeter):
    def __init__(self, name: str, sn: str, reader: AbstractReader, processor: AbstractProcessor):
        super().__init__(
            name=name,
            unit='m3',
            sn=sn,
            reader=reader,
            processor=processor,
        )
