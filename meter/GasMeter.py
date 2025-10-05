import random
from time import sleep
from meter.AbstractMeter import AbstractMeter


class GasMeter(AbstractMeter):
    def __init__(self, name: str, sn: str | None = None):
        super().__init__(name, 'm3', sn)

    def __next__(self) -> float:
        sleep(1)
        return round(random.random() * 5, 2)
