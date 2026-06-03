# Bee Challenge

Physical activity game for kids. A child carries a Badger2040 ("the Bee") and navigates a 4×4 grid of RFID flower tokens, guided by teammates at the "Hive" using a printed reference table. Each turn is two stages: **collect** pollen from one flower, then **deliver** it to a flower of the same type but a different colour, then hand the Bee to the next player. Full design in [docs/design.md](docs/design.md).

## Hardware

| Component | Role |
|---|---|
| Badger2040 (Pi Pico W + e-ink 296×128px) | Main device |
| PN532 NFC/RFID module (I2C, 0x24) | Reads flower + Hive RFID tokens |
| MCP23017 I2C GPIO expander (I2C, 0x20) | Drives 4 arcade buttons via Port B |
| 4× arcade buttons (Red, Blue, Yellow, Green) | Player input |
| 17× RFID tokens | 16 flowers (4 types × 4 colours, all unique) + 1 Hive |

All components share the Badger2040 I2C bus: SDA=GPIO4, SCL=GPIO5.

## Code Structure

```
src/
├── main.py        — game loop entry point; owns I2C setup, BUTTONS config
├── mcp23017.py    — MCP23017 class: read_port_b()
├── pn532.py       — PN532 class: init(), read_passive_target()
├── display.py     — Display class: show_message(), show_idle()
└── tests.py       — standalone Badger built-in button test (not part of game)
```

Instantiate hardware in `main.py`, pass nothing — each class takes `i2c` in its constructor.

## Game State Machine

A turn runs the collect path then the deliver path; both paths share the same
scan → info → button shape.

```
IDLE → WAITING_FOR_HIVE_SCAN
         → SHOWING_COLLECT_TARGET → SHOWING_COLLECT_INFO → POLLEN_COLLECTED
         → SHOWING_DELIVER_TARGET → SHOWING_DELIVER_INFO → POLLEN_DELIVERED
         → WAITING_FOR_HIVE_SCAN (hand off to next player)

Failure (resets the turn → WAITING_FOR_HIVE_SCAN, Eaten++):
  wrong flower scanned → VENUS_FLY_TRAP
  wrong button pressed → SPIDER

Any state → GAME_OVER on timer expiry
```

- Target screens show the current bloom window; the collect target is random,
  the deliver target is fixed by `next_rfid` (same type, different colour).
- **Pollinated** increments on successful delivery only; **Eaten** combines
  spiders and venus fly traps.

## Data Model

```python
flower_map = {
    "<rfid_uid>": {
        "name": "Tulip",
        "colour": "Blue",
        "petals": 5,
        # no correct_button — determined at scan time from random petal count
        "next_uid": "<rfid_uid>",  # deliver target: same type, different colour
        "coordinate": "B3",        # grid label for printed table
    },
}

hive_uid = "<rfid_uid>"

# Each window has its own flower types and petal→button encoding.
# petal_encoding: random count (1–5) shown on device → button to press.
bloom_windows = [
    {"name": "Morning",   "start_seconds": 0,   "map": flower_map_morning,
     "petal_encoding": {1: "Red", 2: "Blue", 3: "Yellow", 4: "Green", 5: "Red"}},
    {"name": "Midday",    "start_seconds": 180, "map": flower_map_midday,
     "petal_encoding": {1: "Yellow", 2: "Green", 3: "Red", 4: "Blue", 5: "Yellow"}},
    {"name": "Afternoon", "start_seconds": 360, "map": flower_map_afternoon,
     "petal_encoding": {1: "Blue", 2: "Yellow", 3: "Green", 4: "Red", 5: "Blue"}},
]
```

## Runtime Notes

- MicroPython on RP2040 — no standard library beyond what's bundled
- e-ink display is slow; use `UPDATE_FAST` and minimise redraws
- Buttons are active-low via MCP23017 Port B pull-ups (`not (port_b & pin)`)
- RFID polling has a short timeout (50ms) to keep the main loop responsive
