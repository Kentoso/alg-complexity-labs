from typing import Optional
from linkedlist import LinkedList
from polynomial_hash import PolynomialHash


class StringSet:
    def __init__(self, size: int = 10**6):
        self.size: int = size
        self.table: list[Optional[LinkedList]] = [None] * self.size
        self.hash_function = PolynomialHash()

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
