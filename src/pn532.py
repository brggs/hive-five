import time


class PN532:
    ADDR = 0x24

    CMD_SAMCONFIGURATION    = 0x14
    CMD_INLISTPASSIVETARGET = 0x4A

    PREAMBLE      = 0x00
    STARTCODE1    = 0x00
    STARTCODE2    = 0xFF
    POSTAMBLE     = 0x00
    HOST_TO_PN532 = 0xD4
    PN532_TO_HOST = 0xD5

    def __init__(self, i2c):
        self.i2c = i2c

    def _write_frame(self, data):
        length = len(data) + 1  # +1 for TFI byte
        lcs = (~length + 1) & 0xFF
        dcs = (~(self.HOST_TO_PN532 + sum(data)) + 1) & 0xFF
        frame = bytes([
            self.PREAMBLE, self.STARTCODE1, self.STARTCODE2,
            length, lcs,
            self.HOST_TO_PN532
        ]) + bytes(data) + bytes([dcs, self.POSTAMBLE])
        self.i2c.writeto(self.ADDR, frame)

    def _read_frame(self, buf):
        if len(buf) < 7:
            print("Buffer too short:", len(buf))
            return None
        if buf[6] != self.PN532_TO_HOST:
            print("Bad TFI:", hex(buf[6]))
            return None
        frame_length = buf[4]
        payload = buf[7: 7 + frame_length - 1]  # -1 to exclude TFI byte
        return payload

    def _send_command(self, cmd, params=None, response_length=0, timeout_ms=500):
        data = [cmd] + (params or [])

        try:
            self._write_frame(data)
        except OSError as e:
            print("Write error:", e)
            return None

        time.sleep_ms(10)

        deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
        ack_received = False
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            try:
                ack = self.i2c.readfrom(self.ADDR, 7)
                if ack[1:7] == bytes([0x00, 0x00, 0xFF, 0x00, 0xFF, 0x00]):
                    ack_received = True
                    break
            except OSError:
                pass
            time.sleep_ms(10)

        if not ack_received:
            print("No ACK received")
            return None

        time.sleep_ms(50)

        deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            try:
                buf = self.i2c.readfrom(self.ADDR, response_length + 8)
                if buf[0] == 0x01:  # ready
                    return self._read_frame(buf)
            except OSError as e:
                print("Read error:", e)
            time.sleep_ms(10)

        print("Response never became ready")
        return None

    def init(self):
        """Configure the PN532 for ISO14443A (NFC/MIFARE) card reading."""
        result = self._send_command(
            self.CMD_SAMCONFIGURATION, [0x01, 0x14, 0x00],
            response_length=1, timeout_ms=500
        )
        print("SAMConfig result:", result)
        return result is not None

    def read_passive_target(self, timeout_ms=100):
        """Poll for a single ISO14443A tag. Returns UID as a hex string, or None."""
        result = self._send_command(
            self.CMD_INLISTPASSIVETARGET,
            [0x01, 0x00],  # max 1 target, 106 kbps ISO14443A
            response_length=20,
            timeout_ms=timeout_ms
        )
        if result is None or len(result) < 5:
            return None
        if result[0] == 0:
            return None
        uid_length = result[4]
        uid_bytes = result[5: 5 + uid_length]
        return ":".join("{:02X}".format(b) for b in uid_bytes)
