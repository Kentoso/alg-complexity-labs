class CRC:
    def __init__(self, polynomial):
        self.polynomial = [int(bit) for bit in polynomial]
        self.poly_len = len(self.polynomial)
        self.poly_deg = self.poly_len - 1
        self.crc_table = self._create_crc_table()

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
