from unittest.mock import MagicMock

from processor.NoneProcessor import NoneProcessor
from processor.PassProcessor import PassProcessor
from processor.DSMRElectricityProcessor import DSMRElectricityProcessor
from processor.DSMRGasProcessor import DSMRGasProcessor


class TestNoneProcessor:
    def test_returns_none(self):
        processor = NoneProcessor()
        assert processor(42) is None

    def test_returns_none_for_string_input(self):
        processor = NoneProcessor()
        assert processor("hello") is None

    def test_returns_none_for_none_input(self):
        processor = NoneProcessor()
        assert processor(None) is None

    def test_is_callable(self):
        processor = NoneProcessor()
        assert callable(processor)


class TestPassProcessor:
    def test_returns_none(self):
        processor = PassProcessor()
        result = processor(42)
        assert result is None

    def test_returns_none_for_string_input(self):
        processor = PassProcessor()
        assert processor("data") is None

    def test_returns_none_for_none_input(self):
        processor = PassProcessor()
        assert processor(None) is None

    def test_is_callable(self):
        processor = PassProcessor()
        assert callable(processor)


class TestDSMRElectricityProcessor:
    def test_returns_none(self, telegram):
        assert DSMRElectricityProcessor()(telegram) is None

    def test_prints_electricity_line(self, telegram, capsys):
        DSMRElectricityProcessor()(telegram)
        assert capsys.readouterr().out.startswith('electricity')

    def test_prints_serial_number(self, telegram, capsys):
        DSMRElectricityProcessor()(telegram)
        assert 'sn=4530303334303034363639353537343136' in capsys.readouterr().out

    def test_prints_tariff_1(self, telegram, capsys):
        DSMRElectricityProcessor()(telegram)
        assert 't1=1234.567kWh' in capsys.readouterr().out

    def test_prints_tariff_2(self, telegram, capsys):
        DSMRElectricityProcessor()(telegram)
        assert 't2=2345.678kWh' in capsys.readouterr().out

    def test_prints_current_usage(self, telegram, capsys):
        DSMRElectricityProcessor()(telegram)
        assert 'now=1.500kW' in capsys.readouterr().out

    def test_prints_current_delivery(self, telegram, capsys):
        DSMRElectricityProcessor()(telegram)
        assert 'returned=0.000kW' in capsys.readouterr().out


class TestDSMRGasProcessor:
    def test_returns_none(self, telegram):
        assert DSMRGasProcessor()(telegram) is None

    def test_prints_gas_line(self, telegram, capsys):
        DSMRGasProcessor()(telegram)
        assert capsys.readouterr().out.startswith('gas')

    def test_prints_serial_number(self, telegram, capsys):
        DSMRGasProcessor()(telegram)
        assert 'sn=4730303233353631323930333635383137' in capsys.readouterr().out

    def test_prints_reading(self, telegram, capsys):
        DSMRGasProcessor()(telegram)
        assert 'reading=1234.567 m3' in capsys.readouterr().out

    def test_no_output_for_non_gas_device(self, capsys):
        water_device = MagicMock()
        water_device.MBUS_DEVICE_TYPE.value = 7
        mock_telegram = MagicMock()
        mock_telegram.MBUS_DEVICES = [water_device]
        DSMRGasProcessor()(mock_telegram)
        assert capsys.readouterr().out == ''
