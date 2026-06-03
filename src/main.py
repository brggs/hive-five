import machine
import time

from mcp23017 import MCP23017
from pn532 import PN532
from display import Display

I2C_SDA = 4
I2C_SCL = 5

i2c = machine.I2C(0, sda=machine.Pin(I2C_SDA), scl=machine.Pin(I2C_SCL), freq=400_000)

mcp     = MCP23017(i2c)
rfid    = PN532(i2c)
display = Display()

BUTTONS = [
    {"pin": 0x01, "label": "B0", "title": "Button B0", "body": "B0 was pressed!"},
    {"pin": 0x02, "label": "B1", "title": "Button B1", "body": "B1 was pressed!"},
    {"pin": 0x04, "label": "B2", "title": "Button B2", "body": "B2 was pressed!"},
    {"pin": 0x08, "label": "B3", "title": "Button B3", "body": "B3 was pressed!"},
]

print("Waiting for PN532 to boot...")
time.sleep_ms(1000)

if not rfid.init():
    display.show_message("PN532 Error", "Check wiring!")
    raise SystemExit

display.show_idle()

prev_button_states = {btn["pin"]: False for btn in BUTTONS}
last_uid = None
uid_display_until = 0

while True:
    now = time.ticks_ms()

    uid = rfid.read_passive_target(timeout_ms=50)
    if uid and uid != last_uid:
        display.show_message("Tag scanned!", uid)
        last_uid = uid
        uid_display_until = time.ticks_add(now, 3000)
    elif not uid:
        last_uid = None

    port_b = mcp.read_port_b()
    any_pressed = False
    newly_released = False

    for btn in BUTTONS:
        pressed = not (port_b & btn["pin"])
        if pressed and not prev_button_states[btn["pin"]]:
            display.show_message(btn["title"], btn["body"])
            uid_display_until = 0
        if not pressed and prev_button_states[btn["pin"]]:
            newly_released = True
        if pressed:
            any_pressed = True
        prev_button_states[btn["pin"]] = pressed

    if newly_released and not any_pressed:
        display.show_idle()

    if uid_display_until and time.ticks_diff(uid_display_until, now) <= 0:
        uid_display_until = 0
        display.show_idle()

    time.sleep_ms(50)
