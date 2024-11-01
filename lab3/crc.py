class CRC:
    def __init__(self, polynomial):
        self.polynomial = [int(bit) for bit in polynomial]
        self.poly_len = len(self.polynomial)
        self.poly_deg = self.poly_len - 1
        self.crc_table = self._create_crc_table()
        self.reflected_polynomial = [int(bit) for bit in polynomial[::-1]]
        self.reflected_polynomial = self.reflected_polynomial[
            self.reflected_polynomial.index(1) :
        ]
        self.reflected_crc_table = self._create_reflected_crc_table()

    def simple(self, message):
        message = [int(bit) for bit in message]
        polynomial_int = int("".join(map(str, self.polynomial)), 2)

        message.extend([0] * self.poly_deg)

        register = 0
        for bit in message:
            register = (register << 1) | bit

            if (register >> self.poly_deg) & 1:
                register ^= polynomial_int

        crc_value = format(register, f"0{self.poly_deg}b")

        return crc_value

    def _create_crc_table(self):
        table = []
        polynomial_int = int("".join(map(str, self.polynomial)), 2)
        for byte in range(256):
            register = byte << (self.poly_deg - 8)
            for _ in range(8):
                if (register & (1 << (self.poly_deg - 1))) != 0:
                    register = (register << 1) ^ polynomial_int
                else:
                    register <<= 1
                register &= (1 << (self.poly_deg + 1)) - 1
            table.append(register & ((1 << self.poly_deg) - 1))
        return table

    def _create_reflected_crc_table(self):
        table = []
        polynomial_int = int("".join(map(str, self.reflected_polynomial)), 2)
        for byte in range(256):
            register = byte
            for _ in range(8):
                if register & 1:
                    register = (register >> 1) ^ (
                        polynomial_int
                        << (self.poly_deg - len(self.reflected_polynomial) + 1)
                    )
                else:
                    register >>= 1
                register &= (1 << self.poly_deg) - 1
            table.append(register)
        return table

    def _bits_to_bytes(self, bits):
        padding_length = (8 - len(bits) % 8) % 8
        bits_padded = [0] * padding_length + bits

        bytes_list = []
        for i in range(0, len(bits_padded), 8):
            byte = 0
            for bit in bits_padded[i : i + 8]:
                byte = (byte << 1) | bit
            bytes_list.append(byte)
        return bytes_list

    def table(self, message):
        message_bits = [int(bit) for bit in message]
        message_bytes = self._bits_to_bytes(message_bits)

        crc = 0

        for byte in message_bytes:
            index = ((crc >> (self.poly_deg - 8)) ^ byte) & 0xFF
            crc = ((crc << 8) ^ self.crc_table[index]) & ((1 << self.poly_deg) - 1)

        crc_value = format(crc, f"0{self.poly_deg}b")
        return crc_value

    def _reflect_bits(self, value, num_bits):
        result = 0
        for i in range(num_bits):
            if (value >> i) & 1:
                result |= 1 << (num_bits - 1 - i)
        return result

    def _reflect_byte(self, byte):
        return self._reflect_bits(byte, 8)

    def reflected_simple(self, message):
        message = [int(bit) for bit in message]
        polynomial_int = int("".join(map(str, self.polynomial[::-1])), 2)

        message.extend([0] * self.poly_deg)

        register = 0
        for bit in message:
            register = (register >> 1) | (bit << self.poly_deg)

            if register & 1:
                register ^= polynomial_int

        reflected_register = self._reflect_bits(register, self.poly_deg + 1)

        crc_value = format(reflected_register, f"0{self.poly_deg}b")

        return crc_value

    def reflected_table(self, message):
        message_bits = [int(bit) for bit in message]
        message_bytes = self._bits_to_bytes(message_bits)
        message_bytes = [self._reflect_byte(byte) for byte in message_bytes]

        crc = 0

        for byte in message_bytes:
            index = (crc ^ byte) & 0xFF
            crc = (self.reflected_crc_table[index] ^ (crc >> 8)) & (
                (1 << self.poly_deg) - 1
            )

        crc_bits = format(crc, f"0{self.poly_deg}b")
        crc_bits = crc_bits[::-1]
        crc_value = crc_bits
        return crc_value
