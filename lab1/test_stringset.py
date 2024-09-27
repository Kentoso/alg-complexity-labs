import pytest
import random
import string

from stringset import StringSet


@pytest.fixture
def string_set():
    return StringSet()


def test_insert_and_search(string_set):
    string_set.insert("apple")
    assert string_set.search("apple")
    assert not string_set.search("banana")


def test_insert_duplicates(string_set):
    string_set.insert("apple")
    string_set.insert("apple")  # Inserting the same string again
    assert string_set.search("apple")


def test_delete(string_set):
    string_set.insert("apple")
    assert string_set.search("apple")
    string_set.delete("apple")
    assert not string_set.search("apple")


def test_delete_non_existing(string_set):
    assert not string_set.delete("banana")  # Deleting a non-existing item


def test_search_non_existing(string_set):
    assert not string_set.search("banana")


def test_validate_string_length(string_set):
    with pytest.raises(ValueError):
        string_set.insert("thisisaverylongstring")  # More than 15 characters


def test_validate_invalid_characters(string_set):
    with pytest.raises(ValueError):
        string_set.insert("Apple123")  # Invalid characters


def test_insert_and_search_multiple_strings(string_set):
    string_set.insert("apple")
    string_set.insert("banana")
    string_set.insert("cherry")
    assert string_set.search("apple")
    assert string_set.search("banana")
    assert string_set.search("cherry")
    assert not string_set.search("date")


def test_insert_and_delete_multiple_strings(string_set):
    string_set.insert("apple")
    string_set.insert("banana")
    string_set.insert("cherry")
    string_set.delete("banana")
    assert string_set.search("apple")
    assert not string_set.search("banana")
    assert string_set.search("cherry")


def test_empty_table_search(string_set):
    assert not string_set.search("apple")


def is_palindrome(s):
    return s == s[::-1]


def find_palindromes_brute_force(s):
    n = len(s)
    palindromes = set()
    for l in range(n):
        for r in range(l, n):
            substr = s[l : r + 1]
            if is_palindrome(substr):
                palindromes.add(substr)
    return palindromes


def test_find_all_palindromes(string_set):
    max_string_length = 15
    num_strings = 10
    random_strings = []

    for _ in range(num_strings):
        length = random.randint(1, max_string_length)
        random_str = "".join(random.choices(string.ascii_lowercase, k=length))
        random_strings.append(random_str)

    expected_palindromes = set()

    for s in random_strings:
        string_set.insert(s)
        expected_palindromes.update(find_palindromes_brute_force(s))

    actual_palindromes = set(string_set.find_all_palindromes())

    assert (
        actual_palindromes == expected_palindromes
    ), f"Failed on strings: {random_strings}"
