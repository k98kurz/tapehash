from .algos import tapehash1, tapehash2, tapehash3, license
from .work import (
    HasNonceProtocol,
    null_prefix_len,
    calculate_difficulty,
    check_difficulty,
    work
)
del algos
