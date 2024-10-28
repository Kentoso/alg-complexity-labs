class CRC:
    def __init__(self, polynomial):
        self.polynomial = [int(bit) for bit in polynomial]
        self.poly_len = len(self.polynomial)
        self.poly_deg = self.poly_len - 1
        self.crc_table = self._create_crc_table()
        self.reflected_polynomial = [int(bit) for bit in polynomial[::-1]]
        self.reflected_crc_table = self._create_reflected_crc_table()

    def simple(self, message):
        message = [int(bit) for bit in message]

        message.extend([0] * self.poly_deg)

        register = message[: self.poly_len]

        for i in range(len(message) - self.poly_deg):
            if register[0] == 1:
                register = [
                    reg_bit ^ poly_bit
                    for reg_bit, poly_bit in zip(register, self.polynomial)
                ]

            if i + self.poly_len < len(message):
                register = register[1:] + [message[i + self.poly_len]]
            else:
                register = register[1:] + [0]

        crc_value = "".join(str(bit) for bit in register[: self.poly_deg])
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
        reflected_poly = int("".join(map(str, self.reflected_polynomial)), 2)

        for dividend in range(256):
            cur_byte = dividend << (self.poly_deg - 8)
            for _ in range(8):
                if cur_byte & (1 << (self.poly_deg - 1)):
                    cur_byte = (
                        (cur_byte << 1) & ((1 << self.poly_deg) - 1)
                    ) ^ reflected_poly
                else:
                    cur_byte = (cur_byte << 1) & ((1 << self.poly_deg) - 1)
            table.append(cur_byte)
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
        message.extend([0] * self.poly_deg)

        register = message[: self.poly_len]

        for i in range(len(message) - self.poly_deg):
            if register[-1] == 1:
                for j in range(self.poly_len):
                    register[-(j + 1)] ^= self.polynomial[j]

            if i + self.poly_len < len(message):
                register = [message[i + self.poly_len]] + register[:-1]
            else:
                register = [0] + register[:-1]

        crc_value = "".join(str(bit) for bit in register[: self.poly_deg])
        return crc_value

    def reflected_table(self, message):
        return self.table(message[::-1])
