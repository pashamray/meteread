from processor import AbstractProcessor

GAS_DEVICE_TYPE = 3


class DSMRGasProcessor(AbstractProcessor):
    def __call__(self, data) -> None:
        for device in data.MBUS_DEVICES:
            if device.MBUS_DEVICE_TYPE.value == GAS_DEVICE_TYPE:
                sn = device.MBUS_EQUIPMENT_IDENTIFIER.value
                reading = device.MBUS_METER_READING
                print(f"gas sn={sn} reading={reading.value} {reading.unit}")
                return
