from typing import Optional
from linkedlist import LinkedList
from polynomial_hash import PolynomialHash


class StringSet:
    def __init__(self, size: int = 10**6):
        self.size: int = size
        self.table: list[Optional[LinkedList]] = [None] * self.size
        self.hash_function = PolynomialHash()
        self.mod = self.hash_function.mod
        self.base = self.hash_function.base

    def validate_string(self, key: str) -> None:
        if len(key) > 15 or not key.islower() or not key.isalpha():
            raise ValueError(
                "String must be at most 15 characters long and contain only lowercase letters a-z"
            )

    def get_hash_index(self, key: str) -> int:
        hash_value = self.hash_function.compute_hash(key)
        return hash_value % self.size

    def insert(self, key: str) -> bool:
        self.validate_string(key)
        index = self.get_hash_index(key)
        if self.table[index] is None:
            self.table[index] = LinkedList()
        if not self.table[index].search(key):
            self.table[index].insert(key)
            return True
        return False

    def search(self, key: str) -> bool:
        self.validate_string(key)
        index = self.get_hash_index(key)
        if self.table[index] is None:
            return False
        return self.table[index].search(key)

    def delete(self, key: str) -> bool:
        self.validate_string(key)
        index = self.get_hash_index(key)
        if self.table[index] is None:
            return False
        if self.table[index].delete(key):
            if self.table[index].is_empty():
                self.table[index] = None
            return True
        return False

    def modinv(self, a: int) -> int:
        return pow(a, self.mod - 2, self.mod)

    def substring_hash(
        self, prefix_hashes: list[int], l: int, r: int, mod_inv_base_powers: list[int]
    ) -> int:
        h_r = prefix_hashes[r]
        h_l_minus_1 = prefix_hashes[l - 1] if l > 0 else 0
        hash_lr = (h_r - h_l_minus_1) % self.mod
        hash_lr = (hash_lr * mod_inv_base_powers[l]) % self.mod
        return hash_lr

    def _find_palindromes(self, s: str) -> set[str]:
        n = len(s)
        self.validate_string(s)

        prefix_hashes_s = self.hash_function.compute_prefix_hashes(s)
        prefix_hashes_rev_s = self.hash_function.compute_prefix_hashes(s[::-1])
        base_powers = self.hash_function.base_powers[: n + 1]

        mod_inv_base_powers = [self.modinv(bp) for bp in base_powers]

        palindromes = set()

        # Odd-length palindromes
        for center in range(n):
            low, high = 0, min(center, n - center - 1)
            while low <= high:
                mid = (low + high) // 2
                l = center - mid
                r = center + mid
                if l < 0 or r >= n:
                    high = mid - 1
                    continue
                hash_lr = self.substring_hash(
                    prefix_hashes_s, l, r, mod_inv_base_powers
                )
                rev_l = n - r - 1
                rev_r = n - l - 1
                if rev_l > rev_r or rev_l < 0 or rev_r >= n:
                    high = mid - 1
                    continue
                hash_rev_lr = self.substring_hash(
                    prefix_hashes_rev_s, rev_l, rev_r, mod_inv_base_powers
                )
                if hash_lr == hash_rev_lr:
                    palindromes.add(s[l : r + 1])
                    low = mid + 1
                else:
                    high = mid - 1

        # Even-length palindromes
        for center in range(n - 1):
            low, high = 0, min(center, n - center - 2)
            while low <= high:
                mid = (low + high) // 2
                l = center - mid
                r = center + mid + 1
                if l < 0 or r >= n:
                    high = mid - 1
                    continue
                if l > r:
                    break
                hash_lr = self.substring_hash(
                    prefix_hashes_s, l, r, mod_inv_base_powers
                )
                rev_l = n - r - 1
                rev_r = n - l - 1
                if rev_l > rev_r or rev_l < 0 or rev_r >= n:
                    high = mid - 1
                    continue
                hash_rev_lr = self.substring_hash(
                    prefix_hashes_rev_s, rev_l, rev_r, mod_inv_base_powers
                )
                if hash_lr == hash_rev_lr:
                    palindromes.add(s[l : r + 1])
                    low = mid + 1
                else:
                    high = mid - 1
        return palindromes

    def find_all_palindromes(self) -> list[str]:
        palindromes = set()
        for ll in self.table:
            if ll:
                current = ll.head
                while current:
                    palindromes |= self._find_palindromes(current.data)
                    current = current.next
        return sorted(palindromes)
