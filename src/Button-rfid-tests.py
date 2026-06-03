import badger2040
import machine
import time

# --- I2C setup ---
I2C_SDA = 4
I2C_SCL = 5

i2c = machine.I2C(0, sda=machine.Pin(I2C_SDA), scl=machine.Pin(I2C_SCL), freq=400_000)

# =============================================================================
# MCP23017
# =============================================================================
MCP23017_ADDR = 0x20
IODIRB = 0x01
GPPUB  = 0x0D
GPIOB  = 0x13

def mcp_write(reg, value):
    i2c.writeto_mem(MCP23017_ADDR, reg, bytes([value]))

def mcp_read(reg):
    return i2c.readfrom_mem(MCP23017_ADDR, reg, 1)[0]

mcp_write(IODIRB, 0xFF)
mcp_write(GPPUB,  0xFF)

BUTTONS = [
    {"pin": 0x01, "label": "B0", "title": "Button B0", "body": "B0 was pressed!"},
    {"pin": 0x02, "label": "B1", "title": "Button B1", "body": "B1 was pressed!"},
    {"pin": 0x04, "label": "B2", "title": "Button B2", "body": "B2 was pressed!"},
    {"pin": 0x08, "label": "B3", "title": "Button B3", "body": "B3 was pressed!"},
]

# =============================================================================
# PN532 minimal I2C driver
# =============================================================================
PN532_ADDR = 0x24

# Command bytes
CMD_SAMCONFIGURATION = 0x14
CMD_INLISTPASSIVETARGET = 0x4A

# Frame bytes
PREAMBLE   = 0x00
STARTCODE1 = 0x00
STARTCODE2 = 0xFF
POSTAMBLE  = 0x00
HOST_TO_PN532 = 0xD4
PN532_TO_HOST = 0xD5

def pn532_write_frame(data):
    """Send a command frame to the PN532 over I2C."""
    length = len(data) + 1  # +1 for TFI byte
    lcs = (~length + 1) & 0xFF
    dcs = (~(HOST_TO_PN532 + sum(data)) + 1) & 0xFF
    frame = bytes([
        PREAMBLE, STARTCODE1, STARTCODE2,  # 0x00, 0x00, 0xFF
        length, lcs,
        HOST_TO_PN532                       # TFI = 0xD4
    ]) + bytes(data) + bytes([dcs, POSTAMBLE])
    i2c.writeto(PN532_ADDR, frame)

def pn532_read_ready():
    """Check the PN532 ready byte (first byte of I2C read is a status byte)."""
    status = i2c.readfrom(PN532_ADDR, 1)
    return status[0] == 0x01

def pn532_read_frame(buf):
    """Parse a response frame from an already-read buffer."""
    # buf[0] = ready byte
    # buf[1..3] = preamble + start code (0x00, 0x00, 0xFF)
    # buf[4] = length, buf[5] = lcs, buf[6] = TFI
    if len(buf) < 7:
        print("Buffer too short:", len(buf))
        return None
    if buf[6] != PN532_TO_HOST:
        print("Bad TFI:", hex(buf[6]))
        return None
    frame_length = buf[4]
    payload = buf[7: 7 + frame_length - 1]  # -1 to exclude TFI byte
    print("Payload:", [hex(b) for b in payload])
    return payload

def pn532_send_command(cmd, params=None, response_length=0, timeout_ms=500):
    data = [cmd] + (params or [])

    try:
        pn532_write_frame(data)
    except OSError as e:
        print("Write error:", e)
        return None

    time.sleep_ms(10)

    # Wait for ACK
    deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
    ack_received = False
    while time.ticks_diff(deadline, time.ticks_ms()) > 0:
        try:
            ack = i2c.readfrom(PN532_ADDR, 7)
            print("ACK bytes:", [hex(b) for b in ack])
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

    # Wait for response ready and read in one go
    deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
    while time.ticks_diff(deadline, time.ticks_ms()) > 0:
        try:
            buf = i2c.readfrom(PN532_ADDR, response_length + 8)
            print("Raw response:", [hex(b) for b in buf])
            if buf[0] == 0x01:  # ready
                return pn532_read_frame(buf)
        except OSError as e:
            print("Read error:", e)
        time.sleep_ms(10)

    print("Response never became ready")
    return None

def pn532_init():
    result = pn532_send_command(CMD_SAMCONFIGURATION, [0x01, 0x14, 0x00],
                                response_length=0, timeout_ms=500)
    print("SAMConfig result:", result)
    # Success is an empty payload (b'') not None
    return result is not None

def pn532_read_passive_target(timeout_ms=100):
    """
    Poll for a single ISO14443A tag.
    Returns the UID as a hex string, or None if no tag present.
    """
    result = pn532_send_command(
        CMD_INLISTPASSIVETARGET,
        [0x01, 0x00],          # max 1 target, 106 kbps ISO14443A
        response_length=20,
        timeout_ms=timeout_ms
    )
    if result is None or len(result) < 5:
        return None
    # result[1] = number of targets found
    if result[0] == 0:
        return None
    uid_length = result[4]
    uid_bytes = result[5: 5 + uid_length]
    return ":".join("{:02X}".format(b) for b in uid_bytes)

# =============================================================================
# Badger display
# =============================================================================
display = badger2040.Badger2040()
display.set_update_speed(badger2040.UPDATE_FAST)

def show_message(title, body):
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.set_font("bitmap8")
    display.set_thickness(2)
    display.text(title, 10, 20, scale=3)
    display.set_thickness(1)
    display.text(body,  10, 70, scale=2)
    display.update()

def show_idle():
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.set_font("bitmap8")
    display.text("Waiting...", 10, 20, scale=2)
    display.text("Scan a tag or", 10, 55, scale=2)
    display.text("press a button", 10, 80, scale=2)
    display.update()

def pn532_init():
    """Configure the PN532 for ISO14443A (NFC/MIFARE) card reading."""
    result = pn532_send_command(CMD_SAMCONFIGURATION, [0x01, 0x14, 0x00],
                                 response_length=1, timeout_ms=500)
    print("SAMConfig result:", result)
    return result is not None

# =============================================================================
# Main loop
# =============================================================================
# In your main code, before pn532_init():
print("Waiting for PN532 to boot...")
time.sleep_ms(1000)

if not pn532_init():
    show_message("PN532 Error", "Check wiring!")
    raise SystemExit

show_idle()

prev_button_states = {btn["pin"]: False for btn in BUTTONS}
last_uid = None
uid_display_until = 0

while True:
    now = time.ticks_ms()

    # --- RFID poll ---
    uid = pn532_read_passive_target(timeout_ms=50)
    if uid and uid != last_uid:
        show_message("Tag scanned!", uid)
        last_uid = uid
        uid_display_until = time.ticks_add(now, 3000)  # show for 3 seconds
    elif not uid:
        last_uid = None  # reset so same tag can re-trigger after removal

    # --- Buttons ---
    port_b = mcp_read(GPIOB)
    any_pressed = False
    newly_released = False

    for btn in BUTTONS:
        pressed = not (port_b & btn["pin"])
        if pressed and not prev_button_states[btn["pin"]]:
            show_message(btn["title"], btn["body"])
            uid_display_until = 0  # cancel any RFID display timer
        if not pressed and prev_button_states[btn["pin"]]:
            newly_released = True
        if pressed:
            any_pressed = True
        prev_button_states[btn["pin"]] = pressed

    if newly_released and not any_pressed:
        show_idle()

    # --- Return to idle after RFID display timeout ---
    if uid_display_until and time.ticks_diff(uid_display_until, now) <= 0:
        uid_display_until = 0
        show_idle()

    time.sleep_ms(50)