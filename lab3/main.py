import random
from crc import CRC

K = 9


def main():
    polynomial = "1100000001111"
    print(f"Polynomial: {polynomial}")
    crc_calculator = CRC(polynomial)
    message = random.choices(["0", "1"], k=K)
    # message = "110101100"
    # message = "010111001"
    # message = "01011100"
    message = "110100111"
    print(f"Message: {''.join(message)}")
    crc_simple = crc_calculator.simple(message)
    print(f"Simple: {crc_simple}")
    crc_reflected_simple = crc_calculator.reflected_simple(message)
    print(f"Reflected simple: {crc_reflected_simple}")
    crc_table = crc_calculator.table(message)
    print(f"Table: {crc_table}")
    crc_reflected_table = crc_calculator.reflected_table(message)
    print(f"Reflected table: {crc_reflected_table}")

    assert crc_simple == crc_reflected_simple == crc_table == crc_reflected_table


if __name__ == "__main__":
    main()
