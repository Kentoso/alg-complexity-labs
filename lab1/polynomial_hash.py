class PolynomialHash:
    def __init__(self, base: int = 31, mod: int = 1000000123, limit: int = 15):
        self.base = base
        self.mod = mod
        self.limit = limit
        self.base_powers = self._precompute_base_powers()

    def _precompute_base_powers(self) -> list[int]:
        base_powers = [1] * (self.limit + 1)
        for i in range(1, self.limit + 1):
            base_powers[i] = (base_powers[i - 1] * self.base) % self.mod
        return base_powers

    def _get_char_offset(self, char: str) -> int:
        return ord(char) - ord("a") + 1

    def compute_prefix_hashes(self, s: str) -> list[int]:
        prefix_hashes = []
        hash_value = 0

        for i, char in enumerate(s):
            hash_value = (
                hash_value + self._get_char_offset(char) * self.base_powers[i]
            ) % self.mod
            prefix_hashes.append(hash_value)

        return prefix_hashes

    def compute_hash(self, s: str) -> int:
        prefix_hashes = self.compute_prefix_hashes(s)
        return prefix_hashes[-1] if prefix_hashes else 0
