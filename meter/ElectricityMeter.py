from meter import AbstractMeter
from processor import AbstractProcessor
from reader import AbstractReader

class ElectricityMeter(AbstractMeter):
    def __init__(self, name: str, sn: str, reader: AbstractReader, processor: AbstractProcessor):
        super().__init__(
            name=name,
            unit='kw/h',
            sn=sn,
            reader=reader,
            processor=processor,
        )
