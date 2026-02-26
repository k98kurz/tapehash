from dataclasses import dataclass, field
from tapehash import (
    tapehash1, tapehash2, tapehash3,
    calculate_difficulty, calculate_target, check_difficulty, work
)
import packify
import unittest


@dataclass
class State:
    data: bytes = field()
    nonce: int = field(default=0)


def serialize(ts: State) -> bytes:
    return packify.pack((ts.data, ts.nonce))

def fakehash_max_difficulty(_: bytes) -> bytes:
    return b'\x00' * 32

def fakehash_min_difficulty(_: bytes) -> bytes:
    return b'\xff' * 32


class TestCalculations(unittest.TestCase):
    def test_calculate_difficulty_e2e(self):
        result = calculate_difficulty(b"\x00" * 32)
        assert isinstance(result, int), result
        assert result == 2**256 - 1, result

        result2 = calculate_difficulty(b"\x01" + b"\x00" * 31)
        assert result2 > 0, result2
        assert result > result2, (result, result2)

        small = calculate_difficulty(b"\x01" + b"\x00" * 31)
        large = calculate_difficulty(b"\x80" + b"\x00" * 31)
        assert small > large, (small, large)

        with self.assertRaises(TypeError):
            calculate_difficulty("test")
        with self.assertRaises(TypeError):
            calculate_difficulty(123)

        result = calculate_target(100)
        assert isinstance(result, int), result
        assert 0 < result < 2**256, result
        assert calculate_target(0) == 2**256 - 1
        assert calculate_target(100) > calculate_target(1000)
        with self.assertRaises(TypeError):
            calculate_target("100")

    def test_check_difficulty_e2e(self):
        result = check_difficulty(b"\x00" * 32, 1)
        assert isinstance(result, bool), result
        assert result is True, result
        assert check_difficulty(b"\xff" * 32, 2**200) is False
        assert check_difficulty(b"\x01" + b"\x00" * 31, 1) is True

        with self.assertRaises(TypeError):
            check_difficulty("test", 100)
        with self.assertRaises(TypeError):
            check_difficulty(b"\x00" * 32, "100")


class TestWork(unittest.TestCase):
    def test_work_e2e(self):
        state = State(b'test')
        result = work(state, serialize, 16, tapehash1)
        assert isinstance(result, State)
        assert check_difficulty(tapehash1(serialize(result)), 16)

    def test_max_attempts(self):
        state = State(b'test')
        work(state, serialize, 2**250, fakehash_min_difficulty, max_attempts=100)
        assert state.nonce <= 100

    def test_type_error(self):
        with self.assertRaises((AttributeError, TypeError)):
            work("not a state", lambda s: bytes([s.nonce]), 100, lambda x: b"")
        with self.assertRaises(TypeError):
            work(State(b'test'), "not callable", 100, lambda x: b"")
        with self.assertRaises(TypeError):
            work(State(b'test'), lambda s: b"", "100", lambda x: b"")
        with self.assertRaises(TypeError):
            work(State(b'test'), lambda s: b"", 100, "not callable")


if __name__ == "__main__":
    unittest.main()
