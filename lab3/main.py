import random
from crc import CRC

K = 1000


def main():
    polynomial = "1100000001111"
    print(f"Polynomial: {polynomial}")
    crc_calculator = CRC(polynomial)
    message = random.choices(["0", "1"], k=K)
    print(f"Message: {''.join(message)}")
    crc = crc_calculator.simple(message)
    print(f"Simple: {crc}")
    crc = crc_calculator.reflected_simple(message)
    print(f"Reflected simple: {crc}")
    crc = crc_calculator.table(message)
    print(f"Table: {crc}")
    crc = crc_calculator.reflected_table(message[::-1])
    print(f"Reflected table: {crc}")


if __name__ == "__main__":
    main()
