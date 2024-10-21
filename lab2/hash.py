import random


class HashFunction:
    def __init__(self, a, b, p) -> None:
        self.a, self.b, self.p = a, b, p

    def hash(self, k: int) -> int:
        return (self.a * k + self.b) % self.p

    def hash_str(self, s: str) -> int:
        k = 0
        for i, char in enumerate(s):
            k += ord(char) * (31**i)
        return self.hash(k)


class HashFunctionGenerator:
    def __init__(self, m) -> None:
        self.m = m
        self.p = self.next_prime(m)

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def next_prime(self, n):
        num = n + 1
        while not self.is_prime(num):
            num += 1
        return int(num)

    def get_hash_function(self) -> HashFunction:
        p = self.p
        a = random.randint(1, p - 1)
        b = random.randint(0, p - 1)
        return HashFunction(a, b, p)
