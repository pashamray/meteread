from meter.AbstractMeter import AbstractMeter
from reader.AbstractReader import AbstractReader

class ElectricityMeter(AbstractMeter):
    def __init__(self, name: str, sn: str, reader: AbstractReader):
        super().__init__(
            name=name,
            unit='kw/h',
            sn=sn,
            reader=reader,
        )
