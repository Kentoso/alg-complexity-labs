class CRC:
    def __init__(self, polynomial):
        self.polynomial = [int(bit) for bit in polynomial]
        self.poly_len = len(self.polynomial)

    def simple(self, message):
        message = [int(bit) for bit in message]

        message.extend([0] * (self.poly_len - 1))

        register = message[: self.poly_len]

        for i in range(len(message) - (self.poly_len - 1)):
            if register[0] == 1:
                register = [
                    reg_bit ^ poly_bit
                    for reg_bit, poly_bit in zip(register, self.polynomial)
                ]

            if i + self.poly_len < len(message):
                register = register[1:] + [message[i + self.poly_len]]
            else:
                register = register[1:] + [0]

        crc_value = "".join(str(bit) for bit in register)
        return crc_value[:-1]
