from processor.AbstractProcessor import AbstractProcessor
from dsmr_parser import telegram_specifications
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5

class DsmrProcessor(AbstractProcessor):
    def __init__(self, device: str = '/dev/ttyUSB0'):
        self.serial_reader = SerialReader(
            device=device,
            serial_settings=SERIAL_SETTINGS_V5,
            telegram_specification=telegram_specifications.V5
        )
        self.telegram_iterator = self.serial_reader.read_as_object()

    def __next__(self) -> float:
        telegram = next(self.telegram_iterator)
        return telegram.CURRENT_ELECTRICITY_USAGE.value
