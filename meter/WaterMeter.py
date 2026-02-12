from meter.AbstractMeter import AbstractMeter
from reader.AbstractReader import AbstractReader

class WaterMeter(AbstractMeter):
    def __init__(self, name: str, sn: str, reader: AbstractReader):
        super().__init__(
            name=name,
            unit='m3',
            reader=reader,
            sn=sn
        )
