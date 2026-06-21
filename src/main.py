import gc
import machine
import sys
import time

from mcp23017 import MCP23017
from pn532 import PN532
from display import Display
import game
from game import Game
import game_data

I2C_SDA = 4
I2C_SCL = 5

i2c = machine.I2C(0, sda=machine.Pin(I2C_SDA), scl=machine.Pin(I2C_SCL), freq=400_000)

_vsys_adc = machine.ADC(29)  # VSYS via on-board 1/3 voltage divider

def read_battery_pct():
    raw = sum(_vsys_adc.read_u16() for _ in range(5)) // 5
    voltage = raw / 65535 * 3.3 * 3
    return max(0, min(100, int((voltage - 3.0) / 1.2 * 100)))

mcp     = MCP23017(i2c)
rfid    = PN532(i2c)
display = Display()

# Arcade buttons on MCP23017 Port A pins 4-7 (active-low via pull-ups). Pin bit -> colour.
# The colour is what Game.on_button() compares against the resolved correct button.
BUTTONS = [
    {"pin": 0x10, "colour": "Green"},
    {"pin": 0x20, "colour": "Yellow"},
    {"pin": 0x40, "colour": "Blue"},
    {"pin": 0x80, "colour": "Red"},
]

# Monotonic seconds for this session (ticks_diff handles the ms-counter wrap).
_prog_start = time.ticks_ms()


def now_s():
    return time.ticks_diff(time.ticks_ms(), _prog_start) / 1000.0


def render(view):
    """Draw the screen for the current Game.view()."""
    state = view["state"]
    p, e = view["pollinated"], view["eaten"]
    if state == game.WAITING_FOR_HIVE_SCAN:
        display.show_waiting(p, e, read_battery_pct())
    elif state in (game.SHOWING_COLLECT_TARGET, game.SHOWING_DELIVER_TARGET):
        display.show_target(view["verb"], view["flower"], view["window"], p, e)
    elif state in (game.SHOWING_COLLECT_INFO, game.SHOWING_DELIVER_INFO):
        display.show_info(view["flower"], view["petals"], view["window"], p, e)
    elif state == game.POLLEN_COLLECTED:
        display.show_collected(p, e)
    elif state == game.POLLEN_DELIVERED:
        display.show_delivered(p, e)
    elif state == game.SPIDER:
        display.show_spider(p, e)
    elif state == game.VENUS_FLY_TRAP:
        display.show_venus(p, e)
    elif state == game.GAME_OVER:
        display.show_game_over(p, e, read_battery_pct())


print("Waiting for PN532 to boot...")
time.sleep_ms(1000)

if not rfid.init():
    display.show_message("PN532 Error", "Check wiring!")
    raise SystemExit

g = Game(game_data.bloom_windows, game_data.hive_uid, game_data.game_duration_seconds)
g.start()

# Reboot automatically if the main loop hangs for more than 5 seconds
# (e.g. a battery knock that locks up the I2C bus). Scores are lost but the
# game is immediately playable again without pressing the physical reset button.
wdt = machine.WDT(timeout=5000)

prev_button_states = {btn["pin"]: False for btn in BUTTONS}
last_uid = None
last_view = None

while True:
    try:
        now = now_s()

        # RFID: act once per fresh tag presentation.
        uid = rfid.read_passive_target(timeout_ms=50)
        if uid and uid != last_uid:
            last_uid = uid
            if uid == game_data.hive_uid:
                g.on_hive_scan(now)
            else:
                g.on_flower_scan(uid, now)
        elif not uid:
            last_uid = None

        # Buttons: act on press edge.
        port_a = mcp.read_port_a()

        # Green + Yellow held together during GAME_OVER restarts the game.
        if g.state == game.GAME_OVER and not (port_a & 0x30):
            g.start(now)
            last_uid = None
            last_view = None

        for btn in BUTTONS:
            pressed = not (port_a & btn["pin"])
            if pressed and not prev_button_states[btn["pin"]]:
                g.on_button(btn["colour"], now)
            prev_button_states[btn["pin"]] = pressed

        g.tick(now)

        # Redraw only when the screen actually changes (e-ink is slow).
        view = g.view()
        if view != last_view:
            render(view)
            last_view = view
    except Exception as e:
        # A transient glitch (e.g. an I2C NACK or a MemoryError) must not freeze
        # the device. Log the traceback to the REPL, surface the exception on the
        # e-ink so a recurrence is diagnosable rather than a blank freeze, then
        # carry on. Force a fresh redraw next loop since last_view is now stale.
        sys.print_exception(e)
        display.show_message("Error", repr(e))
        last_view = None

    gc.collect()
    time.sleep_ms(50)
    wdt.feed()
