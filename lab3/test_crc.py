import pytest
from crc import CRC

polynomial = "1100000001111"


@pytest.mark.parametrize(
    "message, expected_crc",
    [
        ("1101001110111", "011100111010"),
        ("1011101010111", "110001001001"),
        ("1111111111111", "100001111011"),
        ("", "000000000000"),
        ("1", "100000001111"),
    ],
)
def test_crc_simple(message, expected_crc):
    crc_calculator = CRC(polynomial)
    assert (
        crc_calculator.simple(message) == expected_crc
    ), f"Failed for message {message}"


@pytest.mark.parametrize(
    "message, expected_crc",
    [
        ("1101001110111", "011100111010"),
        ("1011101010111", "110001001001"),
        ("1111111111111", "100001111011"),
        ("", "000000000000"),
        ("1", "100000001111"),
    ],
)
def test_crc_table(message, expected_crc):
    crc_calculator = CRC(polynomial)
    assert (
        crc_calculator.table(message) == expected_crc
    ), f"Failed for message {message}"


@pytest.mark.parametrize(
    "message, expected_crc",
    [
        ("1110111001011", "010111001110"),
        ("1110101011101", "100100100011"),
        ("1111111111111", "110111100001"),
        ("", "000000000000"),
    ],
)
def test_crc_reflected_simple(message, expected_crc):
    crc_calculator = CRC(polynomial)
    assert (
        crc_calculator.reflected_simple(message) == expected_crc
    ), f"Failed for message {message}"
