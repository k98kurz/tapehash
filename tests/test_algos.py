import unittest
from tapehash import tapehash1, tapehash2, tapehash3
from tapehash.algos import rotate_tape, execute_opcode


class TestTapehash(unittest.TestCase):
    def test_tapehash1_e2e(self):
        result = tapehash1(b"test")
        assert isinstance(result, bytes), result
        assert len(result) == 32, (len(result), result.hex())

        result2 = tapehash1(b"test")
        assert result == result2, (result.hex(), result2.hex())

        result3 = tapehash1(b"other")
        assert result != result3, (result.hex(), result3.hex())

        with self.assertRaises(TypeError):
            tapehash1("test")
        with self.assertRaises(TypeError):
            tapehash1(123)
        with self.assertRaises(TypeError):
            tapehash1(b"test", code_size="20")
        with self.assertRaises(TypeError):
            tapehash1(b"test", code_size=20.5)
        with self.assertRaises(ValueError):
            tapehash1(b"test", code_size=0)
        with self.assertRaises(ValueError):
            tapehash1(b"test", code_size=-1)
        with self.assertRaises(ValueError):
            tapehash1(b"test", code_size=65_537)

    def test_tapehash2_e2e(self):
        result = tapehash2(b"test")
        assert isinstance(result, bytes), result
        assert len(result) == 32, (len(result), result.hex())

        result2 = tapehash2(b"test")
        assert result == result2, (result.hex(), result2.hex())

        with self.assertRaises(TypeError):
            tapehash2("test")
        with self.assertRaises(TypeError):
            tapehash2(123)
        with self.assertRaises(TypeError):
            tapehash2(b"test", tape_size_multiplier="2")
        with self.assertRaises(TypeError):
            tapehash2(b"test", tape_size_multiplier=2.5)
        with self.assertRaises(ValueError):
            tapehash2(b"test", tape_size_multiplier=0)
        with self.assertRaises(ValueError):
            tapehash2(b"test", tape_size_multiplier=-1)
        with self.assertRaises(ValueError):
            tapehash2(b"test", tape_size_multiplier=65_537)

    def test_tapehash3_e2e(self):
        result = tapehash3(b"test")
        assert isinstance(result, bytes), result
        assert len(result) == 32, (len(result), result.hex())

        result2 = tapehash3(b"test")
        assert result == result2, (result.hex(), result2.hex())

        with self.assertRaises(TypeError):
            tapehash3("test")
        with self.assertRaises(TypeError):
            tapehash3(123)
        with self.assertRaises(TypeError):
            tapehash3(b"test", code_size="64")
        with self.assertRaises(TypeError):
            tapehash3(b"test", code_size=64.5)
        with self.assertRaises(ValueError):
            tapehash3(b"test", code_size=0)
        with self.assertRaises(ValueError):
            tapehash3(b"test", code_size=-1)
        with self.assertRaises(ValueError):
            tapehash3(b"test", code_size=65_537)
        with self.assertRaises(TypeError):
            tapehash3(b"test", tape_size_multiplier="2")
        with self.assertRaises(TypeError):
            tapehash3(b"test", tape_size_multiplier=2.5)
        with self.assertRaises(ValueError):
            tapehash3(b"test", tape_size_multiplier=0)
        with self.assertRaises(ValueError):
            tapehash3(b"test", tape_size_multiplier=-1)
        with self.assertRaises(ValueError):
            tapehash3(b"test", tape_size_multiplier=65_537)


class TestRotateTape(unittest.TestCase):
    def test_rotate(self):
        tape = bytearray(b"\x01\x02\x03\x04\x05")
        assert rotate_tape(tape, 0) == b"\x01\x02\x03\x04\x05"
        assert rotate_tape(tape, 2) == b"\x03\x04\x05\x01\x02"
        assert rotate_tape(tape, 4) == b"\x05\x01\x02\x03\x04"

    def test_errors(self):
        with self.assertRaises(TypeError):
            rotate_tape(b"\x01\x02\x03", 1)
        with self.assertRaises(TypeError):
            rotate_tape([1, 2, 3], 1)
        with self.assertRaises(TypeError):
            rotate_tape(bytearray(b"\x01\x02\x03"), "1")
        with self.assertRaises(TypeError):
            rotate_tape(bytearray(b"\x01\x02\x03"), 1.5)
        with self.assertRaises(ValueError):
            rotate_tape(bytearray(b""), 0)
        with self.assertRaises(ValueError):
            rotate_tape(bytearray(b"\x01\x02\x03"), -1)
        with self.assertRaises(ValueError):
            rotate_tape(bytearray(b"\x01\x02\x03"), 3)


class TestExecuteOpcode(unittest.TestCase):
    def test_math_ops(self):
        val = execute_opcode(0, 0, bytearray(b"\x01"))[0]
        assert val == 1, val
        val = execute_opcode(1, 0, bytearray(b"\x01"))[0]
        assert val == 2, val
        val = execute_opcode(2, 0, bytearray(b"\x02"))[0]
        assert val == 1, val
        val = execute_opcode(3, 0, bytearray(b"\x04"))[0]
        assert val == 2, val
        val = execute_opcode(4, 0, bytearray(b"\x01"))[0]
        assert val == 2, val
        val = execute_opcode(5, 0, bytearray(b"\x00"))[0]
        assert val == 255, val
        val = execute_opcode(6, 0, bytearray(b"\x85"))[0]
        assert val == 10, val
        val = execute_opcode(7, 0, bytearray(b"\x04"))[0]
        assert val == 16, val
        val = execute_opcode(8, 0, bytearray(b"\x08"))[0]
        assert val == 4, val
        val = execute_opcode(9, 0, bytearray(b"\x12"))[0]
        assert val == 33, val

    def test_errors(self):
        with self.assertRaises(TypeError):
            execute_opcode("0", 0, bytearray(b"\x01"))
        with self.assertRaises(TypeError):
            execute_opcode(0, "0", bytearray(b"\x01"))
        with self.assertRaises(TypeError):
            execute_opcode(0, 0, b"\x01")
        with self.assertRaises(ValueError):
            execute_opcode(-1, 0, bytearray(b"\x01"))
        with self.assertRaises(ValueError):
            execute_opcode(16, 0, bytearray(b"\x01"))
        with self.assertRaises(ValueError):
            execute_opcode(0, 10, bytearray(b"\x01"))
        with self.assertRaises(ValueError):
            execute_opcode(0, -1, bytearray(b"\x01"))


if __name__ == "__main__":
    unittest.main()
