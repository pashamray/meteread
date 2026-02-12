from meter.AbstractMeter import AbstractMeter
from reader.AbstractReader import AbstractReader

class GasMeter(AbstractMeter):
    def __init__(self, name: str, sn: str, reader: AbstractReader):
        super().__init__(
            name=name,
            unit='m3',
            sn=sn,
            reader=reader,
        )
