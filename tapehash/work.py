from typing import Protocol, Callable


class HasNonceProtocol(Protocol):
    """The HasNonceProtocol requires that an implementation has a settable
        nonce property.
    """
    @property
    def nonce(self) -> int:
        ...
    @nonce.setter
    def nonce(self, val: int):
        ...

def null_prefix_len(val: bytes) -> int:
    """Returns the number of null prefix bits."""
    total = 0
    idx = 0
    while val[idx] == 0 and idx < len(val):
        total += 8
        idx += 1
    if idx == len(val):
        return total
    val = val[idx]
    if (val & 0b01000000):
        return total + 1
    if (val & 0b00100000):
        return total + 2
    if (val & 0b00010000):
        return total + 3
    if (val & 0b00001000):
        return total + 4
    if (val & 0b00000100):
        return total + 5
    if (val & 0b00000010):
        return total + 6
    if (val & 0b00000001):
        return total + 7
    return total

def calculate_difficulty(val: bytes) -> int:
    """Calculates the difficulty of a hash by counting the preceding
        null bits (null bit prefix) and raising 2 to that number.
    """
    npb = null_prefix_len(val)
    return 2 ** npb

def check_difficulty(val: bytes, difficulty: int) -> bool:
    """Returns True if the val has a difficulty score greater than or
        equal to the supplied difficulty, otherwise False.
    """
    return calculate_difficulty(val) >= difficulty

def work(
    state: HasNonceProtocol, serialize: Callable[[HasNonceProtocol], bytes],
    target: int, hash_algo: Callable[[bytes], bytes]
) -> HasNonceProtocol:
    """Continually increments `state.nonce` until the difficulty score of
        `hash_algo(serialize(state))` >= target, then returns the updated
        state.
    """
    while calculate_difficulty(hash_algo(serialize(state))) < target:
        state.nonce += 1
    return state

