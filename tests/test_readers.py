from unittest.mock import patch, MagicMock

from reader.ZeroReader import ZeroReader
from reader.RandomReader import RandomReader
from reader.DelayReader import DelayReader


class TestZeroReader:
    def test_returns_zero(self):
        reader = ZeroReader()
        assert next(reader) == 0.0

    def test_returns_zero_multiple_times(self):
        reader = ZeroReader()
        for _ in range(5):
            assert next(reader) == 0.0

    def test_return_type_is_float(self):
        reader = ZeroReader()
        assert isinstance(next(reader), float)

    def test_is_iterator(self):
        reader = ZeroReader()
        assert iter(reader) is reader


class TestRandomReader:
    def test_returns_float(self):
        reader = RandomReader()
        value = next(reader)
        assert isinstance(value, float)

    def test_returns_value_in_range(self):
        reader = RandomReader()
        for _ in range(100):
            value = next(reader)
            assert 0.0 <= value <= 5.0

    def test_returns_value_rounded_to_two_decimals(self):
        reader = RandomReader()
        for _ in range(50):
            value = next(reader)
            assert value == round(value, 2)

    @patch("reader.RandomReader.random.random", return_value=0.0)
    def test_returns_zero_when_random_is_zero(self, mock_random):
        reader = RandomReader()
        assert next(reader) == 0.0

    @patch("reader.RandomReader.random.random", return_value=1.0)
    def test_returns_five_when_random_is_one(self, mock_random):
        reader = RandomReader()
        assert next(reader) == 5.0

    @patch("reader.RandomReader.random.random", return_value=0.5)
    def test_returns_two_point_five_when_random_is_half(self, mock_random):
        reader = RandomReader()
        assert next(reader) == 2.5

    def test_is_iterator(self):
        reader = RandomReader()
        assert iter(reader) is reader


class TestDelayReader:
    @patch("reader.DelayReader.sleep")
    def test_delegates_to_wrapped_reader(self, mock_sleep):
        inner = MagicMock()
        inner.__next__ = MagicMock(return_value=42.0)
        reader = DelayReader(inner, delay=0)
        assert next(reader) == 42.0

    @patch("reader.DelayReader.sleep")
    def test_calls_sleep_with_configured_delay(self, mock_sleep):
        inner = MagicMock()
        inner.__next__ = MagicMock(return_value=0.0)
        reader = DelayReader(inner, delay=2.5)
        next(reader)
        mock_sleep.assert_called_once_with(2.5)

    @patch("reader.DelayReader.sleep")
    def test_default_delay_is_one_second(self, mock_sleep):
        inner = MagicMock()
        inner.__next__ = MagicMock(return_value=0.0)
        reader = DelayReader(inner)
        next(reader)
        mock_sleep.assert_called_once_with(1.0)

    @patch("reader.DelayReader.sleep")
    def test_sleep_called_before_read(self, mock_sleep):
        """Verify sleep happens before reading from the inner reader."""
        call_order = []
        mock_sleep.side_effect = lambda _: call_order.append("sleep")
        inner = MagicMock()
        inner.__next__ = MagicMock(
            side_effect=lambda: call_order.append("read") or 0.0
        )
        reader = DelayReader(inner, delay=1.0)
        next(reader)
        assert call_order == ["sleep", "read"]

    @patch("reader.DelayReader.sleep")
    def test_propagates_stop_iteration(self, mock_sleep):
        inner = MagicMock()
        inner.__next__ = MagicMock(side_effect=StopIteration)
        reader = DelayReader(inner)
        try:
            next(reader)
            assert False, "Expected StopIteration"
        except StopIteration:
            pass

    @patch("reader.DelayReader.sleep")
    def test_wraps_zero_reader(self, mock_sleep):
        inner = ZeroReader()
        reader = DelayReader(inner, delay=0)
        assert next(reader) == 0.0

    def test_is_iterator(self):
        inner = MagicMock()
        reader = DelayReader(inner)
        assert iter(reader) is reader
