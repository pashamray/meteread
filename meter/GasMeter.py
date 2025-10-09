from collections.abc import Iterator
from meter.AbstractMeter import AbstractMeter

class GasMeter(AbstractMeter):
    def __init__(self, name: str, processor: Iterator, sn: str | None = None):
        super().__init__(
            name=name,
            unit='m3',
            processor=processor,
            sn=sn
        )
