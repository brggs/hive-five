# Bee Challenge

Physical activity game for kids. A child carries a Badger2040 ("the Bee") and navigates a 4×4 grid of RFID flower tokens, guided by teammates at the "Hive" using a printed reference table. Each turn is two stages: **collect** pollen from one flower, then **deliver** it to a flower of the same type but a different colour, then hand the Bee to the next player. Full design in [docs/design.md](docs/design.md).

## Hardware

| Component | Role |
|---|---|
| Badger2040 (Pi Pico W + e-ink 296×128px) | Main device |
| PN532 NFC/RFID module (I2C, 0x24) | Reads flower + Hive RFID tokens |
| MCP23017 I2C GPIO expander (I2C, 0x20) | Drives 4 arcade buttons via Port A pins 4-7 |
| 4× arcade buttons (Red, Blue, Yellow, Green) | Player input |
| 17× RFID tokens | 16 flowers (4 types × 4 colours, all unique) + 1 Hive |

All components share the Badger2040 I2C bus: SDA=GPIO4, SCL=GPIO5.

## Code Structure

```
src/
├── main.py        — entry point; I2C + hardware setup, BUTTONS, the polling loop
├── game.py        — Game class: state machine + scoring (no hardware imports)
├── game_data.py   — flower maps, bloom_windows, hive_uid, game_duration_seconds
├── mcp23017.py    — MCP23017 class: read_port_b()
├── pn532.py       — PN532 class: init(), read_passive_target()
├── display.py     — Display class: text-only screen methods (one per game screen)
└── tests.py       — desktop unit tests for game.py (run: python3 src/tests.py)
```

Instantiate hardware in `main.py`, pass nothing — each class takes `i2c` in its
constructor. `game.py` is pure logic (imports only `random`) so it runs and is
testable on desktop CPython; `main.py` wires hardware events into it and renders
`Game.view()`.

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
  the deliver target is fixed by `next_uid` (same type, different colour).
- **Pollinated** increments on successful delivery only; **Eaten** combines
  spiders and venus fly traps.

## Data Model

Game data lives in [src/game_data.py](src/game_data.py); the authoritative spec
is [docs/flower-maps.md](docs/flower-maps.md) and [docs/design.md](docs/design.md).
Keep those in sync — don't duplicate the data here.

Key points the code relies on:
- Each `flower_map` entry has `name`, `colour`, `coordinate`, and `next_uid`
  (the deliver target — same type, different colour). Petal count is **not**
  stored: it is a random integer **1–4** generated at each flower scan.
- The button to press is resolved at scan time from
  `petal_encoding[flower_name][petal_count]` — a **per-flower-type** 2D table
  that differs per bloom window (`bloom_windows`, each with `name`,
  `start_seconds`, `map`, `petal_encoding`).

## Runtime Notes

- MicroPython on RP2040 — no standard library beyond what's bundled
- e-ink display is slow; use `UPDATE_FAST` and minimise redraws
- Buttons are active-low via MCP23017 Port A pull-ups (`not (port_a & pin)`)
- RFID polling has a short timeout (50ms) to keep the main loop responsive
