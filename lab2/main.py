from bloom_filter import BloomFilter
from hash import HashFunctionGenerator


def main():
    expected_number_of_elements = 1e6
    false_positive_probability = 0.01

    hash_function_generator = HashFunctionGenerator(expected_number_of_elements)
    print(f"{hash_function_generator.p=}")

    bloom = BloomFilter(
        expected_number_of_elements, false_positive_probability, hash_function_generator
    )
    print(f"{bloom.m=}, {bloom.k=}")
    while True:
        line = input()
        if line == "#":
            break
        if not line:
            continue
        op, word = line[0], line[1:].strip()
        if op == "+":
            bloom.add(word)
        elif op == "?":
            if bloom.check(word):
                print(f"{word}: Y")
            else:
                print(f"{word}: N")


if __name__ == "__main__":
    main()
