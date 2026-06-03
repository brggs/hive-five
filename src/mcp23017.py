class MCP23017:
    IODIRB = 0x01
    GPPUB  = 0x0D
    GPIOB  = 0x13

    def __init__(self, i2c, addr=0x20):
        self.i2c = i2c
        self.addr = addr
        self._write(self.IODIRB, 0xFF)
        self._write(self.GPPUB,  0xFF)

    def _write(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes([value]))

    def _read(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def read_port_b(self):
        return self._read(self.GPIOB)
