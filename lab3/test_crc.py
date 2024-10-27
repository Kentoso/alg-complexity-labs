import pytest
from crc import CRC

polynomial = "1100000001111"


@pytest.mark.parametrize(
    "message, expected_crc",
    [
        ("1101001110111", "011100111010"),  # Example message
        ("1011101010111", "110001001001"),  # Another message example
        ("1111111111111", "100001111011"),  # All ones
        ("0000000000001", "100000001111"),  # All zeros
    ],
)
def test_crc_simple(message, expected_crc):
    crc_calculator = CRC(polynomial)
    assert (
        crc_calculator.simple(message) == expected_crc
    ), f"Failed for message {message}"


def test_crc_empty_message():
    crc_calculator = CRC(polynomial)
    assert (
        crc_calculator.simple("") == "00000000000"
    ), "Empty message should return all-zero CRC"


def test_crc_single_bit_message():
    crc_calculator = CRC(polynomial)
    assert (
        crc_calculator.simple("1") == "100000001111"
    ), "Single-bit message with CRC-12 polynomial should return correct CRC"


def test_crc_different_messages():
    crc_calculator = CRC(polynomial)

    crc1 = crc_calculator.simple("101010101010")
    crc2 = crc_calculator.simple("010101010101")

    assert crc1 != crc2, "CRC values for different messages should not match"


def test_crc_repeated_calculations():
    crc_calculator = CRC(polynomial)
    message = "110100111011"

    crc1 = crc_calculator.simple(message)
    crc2 = crc_calculator.simple(message)

    assert (
        crc1 == crc2
    ), "CRC calculation should be consistent across multiple calls with the same input"
