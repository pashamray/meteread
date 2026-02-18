from processor.NoneProcessor import NoneProcessor
from processor.PassProcessor import PassProcessor


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

    def test_default_sn_is_none_string(self):
        processor = NoneProcessor()
        assert processor.sn == "None"

    def test_default_unit_is_none_string(self):
        processor = NoneProcessor()
        assert processor.unit == "None"

    def test_custom_sn_and_unit(self):
        processor = NoneProcessor(sn="ABC123", unit="kWh")
        assert processor.sn == "ABC123"
        assert processor.unit == "kWh"

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

    def test_default_sn_and_unit(self):
        processor = PassProcessor()
        assert processor.sn == "None"
        assert processor.unit == "None"

    def test_custom_sn_and_unit(self):
        processor = PassProcessor(sn="XYZ", unit="m3")
        assert processor.sn == "XYZ"
        assert processor.unit == "m3"

    def test_is_callable(self):
        processor = PassProcessor()
        assert callable(processor)
