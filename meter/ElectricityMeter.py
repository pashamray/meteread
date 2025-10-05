import random
from time import sleep
from meter.AbstractMeter import AbstractMeter


class ElectricityMeter(AbstractMeter):
    def __init__(self, name: str, sn: str | None = None):
        super().__init__(name, 'kW/h', sn)

    def __next__(self) -> float:
        sleep(1)
        return round(random.random() * 5, 2)
