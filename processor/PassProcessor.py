from typing import Any, Generator
from processor import AbstractProcessor


class PassProcessor(AbstractProcessor):
    def __init__(self, sn: str = 'None', unit: str = 'None'):
        super().__init__(sn, unit)

    def __call__(self, data) -> Generator[dict[str, str | None], Any, None]:
        yield {
            'value' : data,
            'unit' : self.unit,
            'sn' : self.sn,
        }