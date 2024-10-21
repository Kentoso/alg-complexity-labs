import math
from hash import HashFunctionGenerator, HashFunction


class BloomFilter:
    def __init__(
        self,
        expected_elements_num: int,
        false_positive_probability: float,
        hash_function_generator: HashFunctionGenerator,
    ) -> None:
        self.m = int(
            -(expected_elements_num * math.log(false_positive_probability))
            / (math.log(2) ** 2)
        )
        self.k = int((self.m / expected_elements_num) * math.log(2)) + 1
        self.bit_array = [0] * self.m
        self.hash_functions: list[HashFunction] = []
        for _ in range(self.k):
            hf = hash_function_generator.get_hash_function()
            self.hash_functions.append(hf)

    def add(self, item):
        for hf in self.hash_functions:
            digest = hf.hash_str(item) % self.m
            self.bit_array[digest] = 1

    def check(self, item):
        for hf in self.hash_functions:
            digest = hf.hash_str(item) % self.m
            if self.bit_array[digest] == 0:
                return False  # Definitely not in the set
        return True  # Possibly in the set
