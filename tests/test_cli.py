import subprocess
import sys
import shutil
import unittest


def get_command(cmd):
    path = shutil.which(cmd)
    if path:
        return [path]
    return [sys.executable, '-m', f'tapehash.{cmd}']


commands = [
    get_command('tapehash1'), get_command('tapehash2'), get_command('tapehash3')
]


class TestCLI(unittest.TestCase):
    def test_stdin_preimage_equivalence(self):
        for cmd in commands:
            stdin_result = subprocess.run(
                cmd,
                input='test',
                capture_output=True,
                text=True
            )
            preimage_result = subprocess.run(
                cmd + ['--preimage', 'test'],
                capture_output=True,
                text=True
            )
            assert stdin_result.stdout.strip() == preimage_result.stdout.strip(), (
                cmd, stdin_result.stdout, preimage_result.stdout
            )

    def test_code_size_changes_output(self):
        for cmd in [commands[0], commands[2]]:
            result1 = subprocess.run(
                cmd + ['--preimage', 'test'],
                capture_output=True,
                text=True
            )
            result2 = subprocess.run(
                cmd + ['--preimage', 'test', '-cs', '128'],
                capture_output=True,
                text=True
            )
            assert result1.stdout != result2.stdout, (cmd, result1.stdout, result2.stdout)

    def test_tape_size_multiplier_changes_output(self):
        for cmd in [commands[1], commands[2]]:
            result1 = subprocess.run(
                cmd + ['--preimage', 'test'],
                capture_output=True,
                text=True
            )
            result2 = subprocess.run(
                cmd + ['--preimage', 'test', '-tsm', '4'],
                capture_output=True,
                text=True
            )
            assert result1.stdout != result2.stdout, (cmd, result1.stdout, result2.stdout)

    def test_to_raw_outputs_bytes(self):
        result = subprocess.run(
            commands[0] + ['--preimage', 'test', '--to:raw'],
            capture_output=True
        )
        assert len(result.stdout) == 32, len(result.stdout)

        result2 = subprocess.run(
            commands[0] + ['--preimage', 'test'],
            capture_output=True
        )
        assert len(result2.stdout.strip()) == 64, \
            (len(result2.stdout), result2.stdout.strip())
        assert result.stdout.hex() == result2.stdout.strip().decode(), \
            (result.stdout.hex(), result2.stdout.strip().decode())

    def test_difficulty_output(self):
        for cmd in commands:
            result = subprocess.run(
                cmd + ['--preimage', 'test', '--difficulty'],
                capture_output=True,
                text=True
            )
            diff = int(result.stdout.strip())
            assert diff > 0, (cmd, diff)

    def test_check_meets_difficulty(self):
        for cmd in commands:
            result = subprocess.run(
                cmd + ['--preimage', 'test', '--check', '1'],
                capture_output=True,
                text=True
            )
            assert result.stdout.strip() == '1', (cmd, result.stdout)

    def test_check_fails_difficulty(self):
        for cmd in commands:
            result = subprocess.run(
                cmd + ['--preimage', 'test', '--check', '999999'],
                capture_output=True,
                text=True
            )
            assert result.returncode == 2, (cmd, result.returncode)
            assert result.stdout.strip() == '0', (cmd, result.stdout)

    def test_from_hex_input(self):
        for cmd in [commands[0], commands[1]]:
            result1 = subprocess.run(
                cmd + ['--preimage', 'test'],
                capture_output=True,
                text=True
            )
            result2 = subprocess.run(
                cmd + ['--preimage', '74657374', '--from:hex'],
                capture_output=True,
                text=True
            )
            assert result1.stdout == result2.stdout, (cmd, result1.stdout, result2.stdout)


if __name__ == "__main__":
    unittest.main()
