class MCP23017:
    IODIRA = 0x00
    IODIRB = 0x01
    GPPUA  = 0x0C
    GPPUB  = 0x0D
    GPIOA  = 0x12
    GPIOB  = 0x13

    def __init__(self, i2c, addr=0x20):
        self.i2c = i2c
        self.addr = addr
        self._write(self.IODIRA, 0xFF)
        self._write(self.GPPUA,  0xFF)
        self._write(self.IODIRB, 0xFF)
        self._write(self.GPPUB,  0xFF)

    def _write(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes([value]))

    def _read(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def read_port_a(self):
        return self._read(self.GPIOA)

    def read_port_b(self):
        return self._read(self.GPIOB)
