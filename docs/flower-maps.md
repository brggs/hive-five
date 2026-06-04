# Bee Challenge — Flower Maps

Three bloom windows, each with its own set of 4 flower types (loosely themed to real bloom times). The 16 physical RFID tokens never move — each window remaps them to a completely different set of flower identities.

**4 types × 4 colours = 16 unique flowers per window.**

| Window | Flower types |
|---|---|
| Morning   | Tulip, Daisy, Poppy, Bluebell |
| Midday    | Sunflower, Marigold, Rose, Lavender |
| Afternoon | Dahlia, Foxglove, Buttercup, Clover |

---

## Token UIDs

Scan each physical token once and fill in the UIDs below before the game is used.

| Position | UID | Position | UID |
|---|---|---|---|
| A1 | `UID_A1` | C1 | `UID_C1` |
| A2 | `UID_A2` | C2 | `UID_C2` |
| A3 | `UID_A3` | C3 | `UID_C3` |
| A4 | `UID_A4` | C4 | `UID_C4` |
| B1 | `UID_B1` | D1 | `UID_D1` |
| B2 | `UID_B2` | D2 | `UID_D2` |
| B3 | `UID_B3` | D3 | `UID_D3` |
| B4 | `UID_B4` | D4 | `UID_D4` |
| Hive | `UID_HIVE` | | |

---

## Printed sheet layout

Each bloom window has **two tables** on its printed sheet:

- **Table 1 — Location**: the Hive looks up the flower name + colour the device shows, to find where the kid should go and where they deliver to.
- **Table 2 — Button**: when the kid shouts the flower name and petal count, the Hive cross-references both in a grid to find which button to press. Petal counts are **randomly generated** (1–4) by the device each time a flower is scanned — they are not fixed. Table 2 changes each window, so the Hive must use the correct sheet.

---

## Morning (0:00 – 3:00)

*Types: Tulip · Daisy · Poppy · Bluebell*

### Grid

```
       1              2              3              4
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
A │  Red Tulip   │  Red Daisy   │  Red Poppy   │ Red Bluebell │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
B │  Blue Tulip  │  Blue Daisy  │  Blue Poppy  │Blue Bluebell │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
C │ Yellow Tulip │ Yellow Daisy │ Yellow Poppy │Yel Bluebell  │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
D │ Green Tulip  │ Green Daisy  │ Green Poppy  │Grn Bluebell  │
  └──────────────┴──────────────┴──────────────┴──────────────┘
```

### Table 1 — Location *(sorted by flower, then colour)*

| Flower | Colour | Collect from | Deliver to |
|---|---|---|---|
| Bluebell | Blue   | B4 | C4 |
| Bluebell | Green  | D4 | A4 |
| Bluebell | Red    | A4 | B4 |
| Bluebell | Yellow | C4 | D4 |
| Daisy    | Blue   | B2 | C2 |
| Daisy    | Green  | D2 | A2 |
| Daisy    | Red    | A2 | B2 |
| Daisy    | Yellow | C2 | D2 |
| Poppy    | Blue   | B3 | C3 |
| Poppy    | Green  | D3 | A3 |
| Poppy    | Red    | A3 | B3 |
| Poppy    | Yellow | C3 | D3 |
| Tulip    | Blue   | B1 | C1 |
| Tulip    | Green  | D1 | A1 |
| Tulip    | Red    | A1 | B1 |
| Tulip    | Yellow | C1 | D1 |

### Table 2 — Button *(kid shouts flower name + petal count, Hive finds the button)*

| Flower↓ \ Petals→ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Tulip    | **Red**    | **Blue**   | **Yellow** | **Green**  |
| Daisy    | **Blue**   | **Yellow** | **Green**  | **Red**    |
| Poppy    | **Yellow** | **Green**  | **Red**    | **Blue**   |
| Bluebell | **Green**  | **Red**    | **Blue**   | **Yellow** |

---

## Midday (3:00 – 6:00)

*Types: Sunflower · Marigold · Rose · Lavender*

### Grid

```
       1              2              3              4
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
A │Blue Sunflower│ Blue Marigold│   Blue Rose  │Blue Lavender │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
B │Grn Sunflower │Grn Marigold  │  Green Rose  │Grn Lavender  │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
C │ Red Sunflower│ Red Marigold │   Red Rose   │ Red Lavender │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
D │Yel Sunflower │Yel Marigold  │ Yellow Rose  │Yel Lavender  │
  └──────────────┴──────────────┴──────────────┴──────────────┘
```

### Table 1 — Location *(sorted by flower, then colour)*

| Flower | Colour | Collect from | Deliver to |
|---|---|---|---|
| Lavender  | Blue   | A4 | B4 |
| Lavender  | Green  | B4 | C4 |
| Lavender  | Red    | C4 | D4 |
| Lavender  | Yellow | D4 | A4 |
| Marigold  | Blue   | A2 | B2 |
| Marigold  | Green  | B2 | C2 |
| Marigold  | Red    | C2 | D2 |
| Marigold  | Yellow | D2 | A2 |
| Rose      | Blue   | A3 | B3 |
| Rose      | Green  | B3 | C3 |
| Rose      | Red    | C3 | D3 |
| Rose      | Yellow | D3 | A3 |
| Sunflower | Blue   | A1 | B1 |
| Sunflower | Green  | B1 | C1 |
| Sunflower | Red    | C1 | D1 |
| Sunflower | Yellow | D1 | A1 |

### Table 2 — Button *(kid shouts flower name + petal count, Hive finds the button)*

| Flower↓ \ Petals→ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Sunflower | **Yellow** | **Green**  | **Red**    | **Blue**   |
| Marigold  | **Green**  | **Red**    | **Blue**   | **Yellow** |
| Rose      | **Red**    | **Blue**   | **Yellow** | **Green**  |
| Lavender  | **Blue**   | **Yellow** | **Green**  | **Red**    |

---

## Afternoon (6:00 – end)

*Types: Dahlia · Foxglove · Buttercup · Clover*

### Grid

```
       1              2              3              4
  ┌──────────────┬──────────────┬──────────────┬──────────────┐
A │Yellow Dahlia │Yel Foxglove  │Yel Buttercup │ Yel Clover   │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
B │  Red Dahlia  │ Red Foxglove │ Red Buttercup│  Red Clover  │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
C │ Green Dahlia │Grn Foxglove  │Grn Buttercup │ Grn Clover   │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
D │ Blue Dahlia  │Blue Foxglove │Blue Buttercup│  Blue Clover │
  └──────────────┴──────────────┴──────────────┴──────────────┘
```

### Table 1 — Location *(sorted by flower, then colour)*

| Flower    | Colour | Collect from | Deliver to |
|---|---|---|---|
| Buttercup | Blue   | D3 | A3 |
| Buttercup | Green  | C3 | D3 |
| Buttercup | Red    | B3 | C3 |
| Buttercup | Yellow | A3 | B3 |
| Clover    | Blue   | D4 | A4 |
| Clover    | Green  | C4 | D4 |
| Clover    | Red    | B4 | C4 |
| Clover    | Yellow | A4 | B4 |
| Dahlia    | Blue   | D1 | A1 |
| Dahlia    | Green  | C1 | D1 |
| Dahlia    | Red    | B1 | C1 |
| Dahlia    | Yellow | A1 | B1 |
| Foxglove  | Blue   | D2 | A2 |
| Foxglove  | Green  | C2 | D2 |
| Foxglove  | Red    | B2 | C2 |
| Foxglove  | Yellow | A2 | B2 |

### Table 2 — Button *(kid shouts flower name + petal count, Hive finds the button)*

| Flower↓ \ Petals→ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Dahlia    | **Blue**   | **Yellow** | **Green**  | **Red**    |
| Foxglove  | **Yellow** | **Green**  | **Red**    | **Blue**   |
| Buttercup | **Green**  | **Red**    | **Blue**   | **Yellow** |
| Clover    | **Red**    | **Blue**   | **Yellow** | **Green**  |

---

## Python Data

Replace `UID_XX` values with real scanned UIDs. `next_uid` is the delivery target (same type, different colour). The button to press is **not stored per flower** — it is determined at runtime from `petal_encoding[flower_name][petal_count]`, where petal count is randomly generated (1–4) at each scan.

```python
flower_map_morning = {
    "UID_A1": {"name": "Tulip",    "colour": "Red",    "coordinate": "A1", "next_uid": "UID_B1"},
    "UID_A2": {"name": "Daisy",    "colour": "Red",    "coordinate": "A2", "next_uid": "UID_B2"},
    "UID_A3": {"name": "Poppy",    "colour": "Red",    "coordinate": "A3", "next_uid": "UID_B3"},
    "UID_A4": {"name": "Bluebell", "colour": "Red",    "coordinate": "A4", "next_uid": "UID_B4"},
    "UID_B1": {"name": "Tulip",    "colour": "Blue",   "coordinate": "B1", "next_uid": "UID_C1"},
    "UID_B2": {"name": "Daisy",    "colour": "Blue",   "coordinate": "B2", "next_uid": "UID_C2"},
    "UID_B3": {"name": "Poppy",    "colour": "Blue",   "coordinate": "B3", "next_uid": "UID_C3"},
    "UID_B4": {"name": "Bluebell", "colour": "Blue",   "coordinate": "B4", "next_uid": "UID_C4"},
    "UID_C1": {"name": "Tulip",    "colour": "Yellow", "coordinate": "C1", "next_uid": "UID_D1"},
    "UID_C2": {"name": "Daisy",    "colour": "Yellow", "coordinate": "C2", "next_uid": "UID_D2"},
    "UID_C3": {"name": "Poppy",    "colour": "Yellow", "coordinate": "C3", "next_uid": "UID_D3"},
    "UID_C4": {"name": "Bluebell", "colour": "Yellow", "coordinate": "C4", "next_uid": "UID_D4"},
    "UID_D1": {"name": "Tulip",    "colour": "Green",  "coordinate": "D1", "next_uid": "UID_A1"},
    "UID_D2": {"name": "Daisy",    "colour": "Green",  "coordinate": "D2", "next_uid": "UID_A2"},
    "UID_D3": {"name": "Poppy",    "colour": "Green",  "coordinate": "D3", "next_uid": "UID_A3"},
    "UID_D4": {"name": "Bluebell", "colour": "Green",  "coordinate": "D4", "next_uid": "UID_A4"},
}

flower_map_midday = {
    "UID_A1": {"name": "Sunflower", "colour": "Blue",   "coordinate": "A1", "next_uid": "UID_B1"},
    "UID_A2": {"name": "Marigold",  "colour": "Blue",   "coordinate": "A2", "next_uid": "UID_B2"},
    "UID_A3": {"name": "Rose",      "colour": "Blue",   "coordinate": "A3", "next_uid": "UID_B3"},
    "UID_A4": {"name": "Lavender",  "colour": "Blue",   "coordinate": "A4", "next_uid": "UID_B4"},
    "UID_B1": {"name": "Sunflower", "colour": "Green",  "coordinate": "B1", "next_uid": "UID_C1"},
    "UID_B2": {"name": "Marigold",  "colour": "Green",  "coordinate": "B2", "next_uid": "UID_C2"},
    "UID_B3": {"name": "Rose",      "colour": "Green",  "coordinate": "B3", "next_uid": "UID_C3"},
    "UID_B4": {"name": "Lavender",  "colour": "Green",  "coordinate": "B4", "next_uid": "UID_C4"},
    "UID_C1": {"name": "Sunflower", "colour": "Red",    "coordinate": "C1", "next_uid": "UID_D1"},
    "UID_C2": {"name": "Marigold",  "colour": "Red",    "coordinate": "C2", "next_uid": "UID_D2"},
    "UID_C3": {"name": "Rose",      "colour": "Red",    "coordinate": "C3", "next_uid": "UID_D3"},
    "UID_C4": {"name": "Lavender",  "colour": "Red",    "coordinate": "C4", "next_uid": "UID_D4"},
    "UID_D1": {"name": "Sunflower", "colour": "Yellow", "coordinate": "D1", "next_uid": "UID_A1"},
    "UID_D2": {"name": "Marigold",  "colour": "Yellow", "coordinate": "D2", "next_uid": "UID_A2"},
    "UID_D3": {"name": "Rose",      "colour": "Yellow", "coordinate": "D3", "next_uid": "UID_A3"},
    "UID_D4": {"name": "Lavender",  "colour": "Yellow", "coordinate": "D4", "next_uid": "UID_A4"},
}

flower_map_afternoon = {
    "UID_A1": {"name": "Dahlia",     "colour": "Yellow", "coordinate": "A1", "next_uid": "UID_B1"},
    "UID_A2": {"name": "Foxglove",   "colour": "Yellow", "coordinate": "A2", "next_uid": "UID_B2"},
    "UID_A3": {"name": "Buttercup",  "colour": "Yellow", "coordinate": "A3", "next_uid": "UID_B3"},
    "UID_A4": {"name": "Clover",     "colour": "Yellow", "coordinate": "A4", "next_uid": "UID_B4"},
    "UID_B1": {"name": "Dahlia",     "colour": "Red",    "coordinate": "B1", "next_uid": "UID_C1"},
    "UID_B2": {"name": "Foxglove",   "colour": "Red",    "coordinate": "B2", "next_uid": "UID_C2"},
    "UID_B3": {"name": "Buttercup",  "colour": "Red",    "coordinate": "B3", "next_uid": "UID_C3"},
    "UID_B4": {"name": "Clover",     "colour": "Red",    "coordinate": "B4", "next_uid": "UID_C4"},
    "UID_C1": {"name": "Dahlia",     "colour": "Green",  "coordinate": "C1", "next_uid": "UID_D1"},
    "UID_C2": {"name": "Foxglove",   "colour": "Green",  "coordinate": "C2", "next_uid": "UID_D2"},
    "UID_C3": {"name": "Buttercup",  "colour": "Green",  "coordinate": "C3", "next_uid": "UID_D3"},
    "UID_C4": {"name": "Clover",     "colour": "Green",  "coordinate": "C4", "next_uid": "UID_D4"},
    "UID_D1": {"name": "Dahlia",     "colour": "Blue",   "coordinate": "D1", "next_uid": "UID_A1"},
    "UID_D2": {"name": "Foxglove",   "colour": "Blue",   "coordinate": "D2", "next_uid": "UID_A2"},
    "UID_D3": {"name": "Buttercup",  "colour": "Blue",   "coordinate": "D3", "next_uid": "UID_A3"},
    "UID_D4": {"name": "Clover",     "colour": "Blue",   "coordinate": "D4", "next_uid": "UID_A4"},
}

hive_uid = "UID_HIVE"

bloom_windows = [
    {
        "name": "Morning",
        "start_seconds": 0,
        "map": flower_map_morning,
        # petal_encoding[flower_name][petal_count] → button to press
        # petal count is randomly generated 1–4 at each flower scan
        "petal_encoding": {
            "Tulip":    {1: "Red",    2: "Blue",   3: "Yellow", 4: "Green"},
            "Daisy":    {1: "Blue",   2: "Yellow", 3: "Green",  4: "Red"},
            "Poppy":    {1: "Yellow", 2: "Green",  3: "Red",    4: "Blue"},
            "Bluebell": {1: "Green",  2: "Red",    3: "Blue",   4: "Yellow"},
        },
    },
    {
        "name": "Midday",
        "start_seconds": 180,
        "map": flower_map_midday,
        "petal_encoding": {
            "Sunflower": {1: "Yellow", 2: "Green",  3: "Red",    4: "Blue"},
            "Marigold":  {1: "Green",  2: "Red",    3: "Blue",   4: "Yellow"},
            "Rose":      {1: "Red",    2: "Blue",   3: "Yellow", 4: "Green"},
            "Lavender":  {1: "Blue",   2: "Yellow", 3: "Green",  4: "Red"},
        },
    },
    {
        "name": "Afternoon",
        "start_seconds": 360,
        "map": flower_map_afternoon,
        "petal_encoding": {
            "Dahlia":     {1: "Blue",   2: "Yellow", 3: "Green",  4: "Red"},
            "Foxglove":   {1: "Yellow", 2: "Green",  3: "Red",    4: "Blue"},
            "Buttercup":  {1: "Green",  2: "Red",    3: "Blue",   4: "Yellow"},
            "Clover":     {1: "Red",    2: "Blue",   3: "Yellow", 4: "Green"},
        },
    },
]

game_duration_seconds = 600
```
