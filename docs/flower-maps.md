# Bee Challenge — Flower Maps

Three bloom windows, each with its own set of 4 flower types (loosely themed to real bloom times). The 16 physical RFID tokens never move — each window remaps them to a completely different set of flower identities.

**4 types × 4 colours = 16 unique flowers per window.**

Each window uses a scattered layout: every row and every column contains all 4 flower types and all 4 colours. No two positions in the same row or column share a type or colour, so kids cannot predict the grid without the reference table, and delivery paths scatter diagonally across the grid rather than staying in the same column.

| Window | Flower types |
|---|---|
| Morning   | Tulip, Daisy, Poppy, Bluebell |
| Midday    | Sunflower, Marigold, Rose, Lavender |
| Afternoon | Dahlia, Foxglove, Buttercup, Clover |

---

## Token UIDs

Scanned 2026-06-05. These are the real hardware UIDs — edit `token_uids` in `src/game_data.py` if tokens are ever re-scanned.

| Position | UID | Position | UID |
|---|---|---|---|
| A1 | `00:07:04:4D:A4:98:CA:2A:81` | C1 | `00:07:04:44:A4:98:CA:2A:81` |
| A2 | `00:07:04:4F:A4:98:CA:2A:81` | C2 | `00:07:04:36:A4:98:CA:2A:81` |
| A3 | `00:07:04:4E:A4:98:CA:2A:81` | C3 | `00:07:04:45:A4:98:CA:2A:81` |
| A4 | `00:07:04:47:A4:98:CA:2A:81` | C4 | `00:07:04:3B:A4:98:CA:2A:81` |
| B1 | `00:07:04:3D:A4:98:CA:2A:81` | D1 | `00:07:04:46:A4:98:CA:2A:81` |
| B2 | `00:07:04:34:A4:98:CA:2A:81` | D2 | `00:07:04:3C:A4:98:CA:2A:81` |
| B3 | `00:07:04:35:A4:98:CA:2A:81` | D3 | `00:07:04:2B:A4:98:CA:2A:81` |
| B4 | `00:07:04:3E:A4:98:CA:2A:81` | D4 | `00:07:04:2A:A4:98:CA:2A:81` |
| Hive | `00:07:04:2C:A4:98:CA:2A:81` | | |

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
A │  Red Tulip   │  Blue Daisy  │Yellow Poppy  │ Org Bluebell │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
B │Yellow Daisy  │  Org Tulip   │  Red Bluebell│  Blue Poppy  │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
C │  Org Poppy   │ Yel Bluebell │  Blue Tulip  │  Red Daisy   │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
D │Blue Bluebell │  Red Poppy   │  Org Daisy   │  Yel Tulip   │
  └──────────────┴──────────────┴──────────────┴──────────────┘
```

### Table 1 — Location *(sorted by flower, then colour)*

| Flower | Colour | Collect from | Deliver to |
|---|---|---|---|
| Bluebell | Blue   | D1 | A4 |
| Bluebell | Orange  | A4 | B3 |
| Bluebell | Red    | B3 | C2 |
| Bluebell | Yellow | C2 | D1 |
| Daisy    | Blue   | A2 | B1 |
| Daisy    | Orange  | D3 | A2 |
| Daisy    | Red    | C4 | D3 |
| Daisy    | Yellow | B1 | C4 |
| Poppy    | Blue   | B4 | C1 |
| Poppy    | Orange  | C1 | D2 |
| Poppy    | Red    | D2 | A3 |
| Poppy    | Yellow | A3 | B4 |
| Tulip    | Blue   | C3 | D4 |
| Tulip    | Orange  | B2 | C3 |
| Tulip    | Red    | A1 | B2 |
| Tulip    | Yellow | D4 | A1 |

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
A │Blue Sunflower│ Org Marigold │   Red Rose   │Yel Lavender  │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
B │ Red Marigold │Yel Sunflower │Blue Lavender │  Org Rose    │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
C │  Yel Rose    │ Red Lavender │ Org Sunflower│Blue Marigold │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
D │ Org Lavender │   Blue Rose  │Yel Marigold  │ Red Sunflower│
  └──────────────┴──────────────┴──────────────┴──────────────┘
```

### Table 1 — Location *(sorted by flower, then colour)*

| Flower | Colour | Collect from | Deliver to |
|---|---|---|---|
| Lavender  | Blue   | B3 | C2 |
| Lavender  | Orange  | D1 | A4 |
| Lavender  | Red    | C2 | D1 |
| Lavender  | Yellow | A4 | B3 |
| Marigold  | Blue   | C4 | D3 |
| Marigold  | Orange  | A2 | B1 |
| Marigold  | Red    | B1 | C4 |
| Marigold  | Yellow | D3 | A2 |
| Rose      | Blue   | D2 | A3 |
| Rose      | Orange  | B4 | C1 |
| Rose      | Red    | A3 | B4 |
| Rose      | Yellow | C1 | D2 |
| Sunflower | Blue   | A1 | B2 |
| Sunflower | Orange  | C3 | D4 |
| Sunflower | Red    | D4 | A1 |
| Sunflower | Yellow | B2 | C3 |

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
A │ Org Dahlia   │  Red Foxglove│Yel Buttercup │  Blue Clover │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
B │Yel Foxglove  │  Blue Dahlia │  Org Clover  │ Red Buttercup│
  ├──────────────┼──────────────┼──────────────┼──────────────┤
C │Blue Buttercup│  Yel Clover  │  Red Dahlia  │ Org Foxglove │
  ├──────────────┼──────────────┼──────────────┼──────────────┤
D │  Red Clover  │ Org Buttercup│ Blue Foxglove│  Yel Dahlia  │
  └──────────────┴──────────────┴──────────────┴──────────────┘
```

### Table 1 — Location *(sorted by flower, then colour)*

| Flower    | Colour | Collect from | Deliver to |
|---|---|---|---|
| Buttercup | Blue   | C1 | D2 |
| Buttercup | Orange  | D2 | A3 |
| Buttercup | Red    | B4 | C1 |
| Buttercup | Yellow | A3 | B4 |
| Clover    | Blue   | A4 | B3 |
| Clover    | Orange  | B3 | C2 |
| Clover    | Red    | D1 | A4 |
| Clover    | Yellow | C2 | D1 |
| Dahlia    | Blue   | B2 | C3 |
| Dahlia    | Orange  | A1 | B2 |
| Dahlia    | Red    | C3 | D4 |
| Dahlia    | Yellow | D4 | A1 |
| Foxglove  | Blue   | D3 | A2 |
| Foxglove  | Orange  | C4 | D3 |
| Foxglove  | Red    | A2 | B1 |
| Foxglove  | Yellow | B1 | C4 |

### Table 2 — Button *(kid shouts flower name + petal count, Hive finds the button)*

| Flower↓ \ Petals→ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Dahlia    | **Blue**   | **Yellow** | **Green**  | **Red**    |
| Foxglove  | **Yellow** | **Green**  | **Red**    | **Blue**   |
| Buttercup | **Green**  | **Red**    | **Blue**   | **Yellow** |
| Clover    | **Red**    | **Blue**   | **Yellow** | **Green**  |
