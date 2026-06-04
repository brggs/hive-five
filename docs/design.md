# Bee Challenge — Game Design

## Overview

Bee Challenge is a physical activity game for children. One kid carries a handheld device (the "Bee"), which runs on a Badger2040. Each turn, the bee-carrier **collects** pollen from one flower and then **delivers** it to a second flower of the same type — navigating a 4×4 grid of physical flowers (RFID tokens) and pressing the correct coloured arcade button at each one, guided by teammates back at the "Hive" using a printed reference table. The game runs for a fixed time limit; scores track how many flowers were successfully pollinated and how many bees were lost to spiders and venus fly traps.

---

## Hardware

| Component | Purpose |
|---|---|
| Badger2040 (Pi Pico W + e-ink display, 296×128px) | Main device — the "Bee" |
| PN532 NFC/RFID module (13.56MHz, I2C) | Reads RFID tokens on flowers and Hive |
| Adafruit MCP23017 I2C GPIO Expander (STEMMA QT) | Drives the 4 arcade buttons |
| 4× coloured arcade buttons (Red, Blue, Yellow, Green) | Player input — the "pollen colours" |
| 17× RFID tokens | 16 flowers in a 4×4 grid + 1 Hive token |

All components communicate over I2C; the PN532 and MCP23017 share the Badger2040's I2C bus (or STEMMA QT chain).

---

## Physical Setup

### The Flower Grid

Flowers are arranged in a 4×4 grid. Each position is labelled with a coordinate (A1–D4). Each position holds one RFID token representing a flower. The 16 flowers are the 4 types × 4 colours, so **every type+colour combination is unique** — there is exactly one Blue Tulip, one Red Tulip, and so on.

Each flower has three properties:
- **Type**: one of four types (e.g. Rose, Tulip, Dahlia, Sunflower — exact names TBD)
- **Colour**: Red, Blue, Yellow, or Green
- **Petal count**: a small integer, unique enough within the table to disambiguate rows

Each RFID token encodes a **flower ID** that the device maps to these properties.

### The Hive

A fixed base station with its own RFID token. Players scan this token at the start of each turn.

### Printed Reference Table

The Hive team has a physical printed table — one per bloom window (see [Bloom Windows](#bloom-windows) and [flower-maps.md](flower-maps.md)). Each table has one row per flower, with columns:

**Table 1 — Location**: flower name + colour → grid coordinates (where to collect from, where to deliver to).

**Table 2 — Button**: a 4×4 grid of flower type × petal count → button colour. The child shouts both the flower name and the petal count; the Hive cross-references both to find the button.

Together the two tables encode the complete game sequence for each bloom window.

---

## Game Flow

### Turn Structure

Each turn belongs to one player; players take turns holding the Bee. A turn has two stages — **collect** pollen from one flower, then **deliver** it to a second flower of the same type — after which the Bee is handed to the next player.

```
[Start of turn]
  Player scans Hive token
    → Device shows the COLLECT target (flower name + colour) and the current
      bloom window (morning / midday / afternoon), which advances as game time
      passes.
    → Hive team look up that flower's location on the map for the current bloom
      window and shout the coordinate.

[Kid travels to the collect flower]
  Kid scans flower RFID
    Wrong flower  → VENUS FLY TRAP (see below)
    Correct flower → Device shows: flower name, colour, petal count
      → Kid shouts the flower name and petal count back to the Hive
      → Hive looks up flower + petals in Table 2 → shouts the coloured button

[Kid presses button]
  Correct button → POLLEN COLLECTED
    → Device briefly shows a success screen
    → Device shows the DELIVER target: a flower of the same type but a
      different colour
  Wrong button   → SPIDER (see below)

[Kid travels to the deliver flower]
  Kid scans flower RFID
    Wrong flower  → VENUS FLY TRAP (see below)
    Correct flower → Device shows: flower name, colour, petal count
      → Kid shouts the flower name and petal count back to the Hive
      → Hive looks up flower + petals in Table 2 → shouts the coloured button

[Kid presses button]
  Correct button → POLLEN DELIVERED
    → Device briefly shows a success screen
    → Kid returns to the Hive and hands the Bee to the next player
  Wrong button   → SPIDER (see below)
```

### Failure States — Spider & Venus Fly Trap

A turn can fail in two ways:

- **VENUS FLY TRAP** — the kid scans the **wrong flower** (anything that isn't the current target).
- **SPIDER** — the kid presses the **wrong button** at the correct flower.

In both cases:
- The device shows the matching failure screen (venus fly trap or spider)
- The **Eaten** counter is incremented
- The kid returns to the Hive and hands the Bee to the next player
- **The next player starts fresh** — any pollen collected this turn is lost, and a new collect target is re-randomised (see below)

### Hive Scan → Collect Target

When a player scans the Hive token, the device *displays* the turn's **collect** target — it does not generate it on the spot:

- At the **start of the game**, or after a **spider / venus fly trap reset**, the device picks a **random** flower from the current bloom window's flower set as the collect target.
- The matching **deliver** target — a flower of the same type but a different colour — is fixed by the game data (the `next_rfid` / "Deliver to" link) and is revealed only after pollen is collected.

So the Hive scan triggers *display* of the collect target, not its generation; the deliver target is already decided before the kid sets off. Because every turn is a single collect→deliver pair, no progress carries between turns — each new turn starts from a fresh random collect target.

---

## Device States

```
IDLE
  │  game timer starts / reset
  ▼
WAITING_FOR_HIVE_SCAN
  │  Hive RFID scanned
  ▼
SHOWING_COLLECT_TARGET    "Collect from: Blue Tulip" + bloom window
  │  correct flower scanned         (wrong flower → VENUS_FLY_TRAP)
  ▼
SHOWING_COLLECT_INFO      shows petal count; kid shouts it
  │  correct button pressed         (wrong button → SPIDER)
  ▼
POLLEN_COLLECTED          brief success screen
  ▼
SHOWING_DELIVER_TARGET    "Deliver to: Yellow Tulip" (same type)
  │  correct flower scanned         (wrong flower → VENUS_FLY_TRAP)
  ▼
SHOWING_DELIVER_INFO      shows petal count; kid shouts it
  │  correct button pressed         (wrong button → SPIDER)
  ▼
POLLEN_DELIVERED          brief success screen → hand Bee to next player
  ▼
WAITING_FOR_HIVE_SCAN

SPIDER / VENUS_FLY_TRAP ──(brief delay)──► WAITING_FOR_HIVE_SCAN
                         (Eaten++, turn resets, new random collect target)

Any state ──(timer expires)──► GAME_OVER
```

---

## Screens

All screens show the persistent score bar at the bottom.

### WAITING_FOR_HIVE_SCAN
```
┌──────────────────────────────┐
│                              │
│   Hand the Bee to the        │
│   next player!               │
│                              │
│   Scan the Hive to start.    │
│                              │
│  Pollinated: 3 | Eaten: 1    │
└──────────────────────────────┘
```

### SHOWING_COLLECT_TARGET / SHOWING_DELIVER_TARGET
The two target screens share one layout; only the header verb differs
("COLLECT FROM" vs "DELIVER TO"). The header also shows the current bloom
window (☀ Morning / 🌤 Midday / 🌇 Afternoon).
```
┌──────────────────────────────┐
│  COLLECT FROM:    ☀ Morning  │
│                              │
│    🌷 Blue Tulip             │
│                              │
│  (Hive team: check the map!) │
│  Pollinated: 3 | Eaten: 1    │
└──────────────────────────────┘
```
(flower image is a simple bitmap icon for the type)

### SHOWING_COLLECT_INFO / SHOWING_DELIVER_INFO
Shown after the correct flower is scanned. Same layout for both stages.
```
┌──────────────────────────────┐
│  You found:                  │
│                              │
│    🌷 Blue Tulip             │
│    Petals: 3                 │
│                              │
│  Shout flower name & petals! │
│  Pollinated: 3 | Eaten: 1    │
└──────────────────────────────┘
```

### POLLEN_COLLECTED
```
┌──────────────────────────────┐
│                              │
│   ✓ POLLEN COLLECTED!        │
│                              │
│   Now deliver it to          │
│   another flower!            │
│  Pollinated: 3 | Eaten: 1    │
└──────────────────────────────┘
```

### POLLEN_DELIVERED
```
┌──────────────────────────────┐
│   ✓ POLLINATED!              │
│                              │
│   Return to the Hive and     │
│   hand over the Bee.         │
│                              │
│  Pollinated: 4 | Eaten: 1    │
└──────────────────────────────┘
```

### SPIDER (wrong button)
```
┌──────────────────────────────┐
│   🕷 EATEN BY A SPIDER!      │
│   (wrong button)             │
│                              │
│   Return to the Hive.        │
│                              │
│  Pollinated: 3 | Eaten: 2    │
└──────────────────────────────┘
```

### VENUS_FLY_TRAP (wrong flower)
```
┌──────────────────────────────┐
│   🪰 VENUS FLY TRAP!         │
│   (wrong flower)             │
│                              │
│   Return to the Hive.        │
│                              │
│  Pollinated: 3 | Eaten: 2    │
└──────────────────────────────┘
```

### GAME_OVER
```
┌──────────────────────────────┐
│      GAME OVER               │
│                              │
│   Flowers pollinated: 7      │
│   Bees eaten:         3      │
│                              │
│   Well done everyone!        │
└──────────────────────────────┘
```

---

## Scoring

A persistent counter is maintained for the current game session:

- **Pollinated**: incremented once per successful **delivery** (POLLEN DELIVERED). Collecting pollen is a sub-step and does not score on its own — a turn only counts once the pollen has been delivered.
- **Eaten**: incremented each time the bee is lost, whether to a **spider** (wrong button) or a **venus fly trap** (wrong flower). The two failure types are combined into this single total.

Both counters are shown at the bottom of every screen throughout the game and on the final Game Over screen.

---

## Bloom Windows

The game is divided into time-based **bloom windows** — morning, midday, and afternoon — each using a different **flower map**. The current bloom window is shown on the device's target screens and advances automatically as game time passes. A flower map defines, for each grid coordinate:
- Which RFID token sits there
- The flower identity that token represents in this window — name, colour, and petal count
- The lookup-table row for that flower (button to press + the same-type delivery flower)

Bloom windows remap flower **identities**: the physical RFID tokens never move, but the same token represents a completely different flower each window — different type name, colour, and petal encoding. Each window has its own set of 4 flower types, loosely themed to real bloom times:

| Bloom window | Time window | Flower types |
|---|---|---|
| Morning   | 0:00 – 3:00 | Tulip, Daisy, Poppy, Bluebell |
| Midday    | 3:00 – 6:00 | Sunflower, Marigold, Rose, Lavender |
| Afternoon | 6:00 – end  | Dahlia, Foxglove, Buttercup, Clover |

Each window also has its own **petal encoding** (see below) — a 2D table mapping flower type × random petal count to button — so the Hive's button lookup changes each window too.

When the bloom window changes:
- The device silently switches to the new map's lookup data
- If a turn is in progress when the window changes, that turn finishes on the map it began with; the next turn's collect target is drawn from the new map
- The Hive team swaps to the corresponding printed table

Each bloom window has its own printed reference table, labelled clearly with the window name and time.

---

## Data Model (Outline)

```python
# One entry per flower in the current bloom window's map.
# No correct_button here — the button is determined at scan time via
# petal_encoding[flower_name][random_petal_count], where count is 1–4.
flower_map = {
    "<rfid_uid>": {
        "name": "Tulip",          # flower type / species
        "colour": "Blue",
        "next_uid": "<rfid_uid>", # deliver target: same type, different colour
        "coordinate": "B3",       # grid label, shown on printed table
    },
    ...
}

hive_uid = "<rfid_uid>"

# Bloom windows — each has its own flower set and petal encoding.
# petal_encoding[flower_name][petal_count] → button to press.
# petal_count is randomly generated 1–4 at each flower scan.
bloom_windows = [
    {
        "name": "Morning",
        "start_seconds": 0,
        "map": flower_map_morning,
        "petal_encoding": {
            "Tulip":    {1: "Red",    2: "Blue",   3: "Yellow", 4: "Green"},
            "Daisy":    {1: "Blue",   2: "Yellow", 3: "Green",  4: "Red"},
            # ... (see flower-maps.md for full data)
        },
    },
    ...
]

game_duration_seconds = 600  # 10 minutes total
```

---

## Out of Scope (v1)

- Wireless connectivity / score upload
- Sound effects (Badger2040 has no speaker by default)
- Per-player score tracking (only global session totals)
- Dynamic difficulty adjustment
- Admin screen for configuring bloom-window durations or flower maps on-device


## Open Questions
- Exact bloom-window durations and total game length.
- Confirm in-progress-turn behaviour when a bloom window changes (current assumption: the turn finishes on the map it began with).
