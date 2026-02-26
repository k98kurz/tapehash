## 0.1.1

- CLI fixes:
    - tapehash1: corrected help text
    - tapehash2: corrected help text
    - tapehash3:
        - corrected help text
        - uses tapehash3 consistently instead of tapehash1 with `--check` mode
- Added test suite

## 0.1.0

- Initial release.
- Added 3 algorithms:
    - tapehash1: tuneable computational complexity
    - tapehash2: tuneable memory complexity
    - tapehash3: tuneable computational and memory complexity
- Default parameters tuned for 0.25-0.3 ms per hash for all 3
- CLI tool for each algorithm
- Proof-of-work:
    - `HasNonceProtocol`
    - `calculate_difficulty`
    - `calculate_target`
    - `check_difficulty`
    - `work`

