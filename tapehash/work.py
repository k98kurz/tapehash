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

def calculate_difficulty(digest: bytes) -> int:
    """Calculates the difficulty of a hash by dividing 2**256 (max int)
        by the supplied digest interpreted as a big-endian unsigned int.
        This provides a linear metric that represents the expected
        amount of work (hashes) that have to be computed on average to
        reach the given digest or better (lower). Returns 2**256-1 if
        digest is all null bytes.
    """
    val = int.from_bytes(digest, 'big')
    if not val:
        return 2**256 - 1
    return 2**256 // val

def calculate_target(difficulty: int) -> int:
    """Calculates the target value that a hash must be <= to meet
        the difficulty threshold. For difficulty >= 2: 2**256 //
        difficulty - 1; for difficulty <= 1: 2**256 - 1.
    """
    return 2**256 - 1 if not difficulty else 2**256 // difficulty - 1

def check_difficulty(digest: bytes, difficulty: int) -> bool:
    """Returns `True` if `digest` has a difficulty score greater than or
        equal to the supplied difficulty, otherwise `False`.
    """
    return calculate_difficulty(digest) >= difficulty

def work(
        state: HasNonceProtocol, serialize: Callable[[HasNonceProtocol], bytes],
        difficulty: int, hash_algo: Callable[[bytes], bytes],
        max_attempts: int = 10**10
    ) -> HasNonceProtocol:
    """Continually increments `state.nonce` until the difficulty score of
        `hash_algo(serialize(state))` >= target or until `max_attempts`,
        then returns the updated state.
    """
    target = calculate_target(difficulty)
    for _ in range(max_attempts):
        if int.from_bytes(hash_algo(serialize(state)), 'big') <= target:
            break
        state.nonce += 1
    return state

