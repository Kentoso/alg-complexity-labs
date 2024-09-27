import pytest
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
