"""Bee Challenge game data.

Authoritative spec: docs/flower-maps.md and docs/design.md.

The 16 physical RFID tokens never move; each bloom window remaps them to a
different set of flower identities. Tokens are authored by grid coordinate
(A1..D4) and the real hardware UIDs live in exactly one place: `token_uids`.
Re-scanned the tokens? Update `token_uids` and nothing else changes.

The button to press is NOT stored per flower. It is resolved at scan time from
petal_encoding[flower_name][petal_count], where petal_count is a random integer
1-4 generated each time a flower is scanned.
"""

# The ONLY place real hardware UIDs live. UIDs are the hex strings returned by
# PN532.read_passive_target(), e.g. "04:A2:1B:5C". Everything else refers to
# tokens by their grid coordinate.
token_uids = {
    "A1": "00:07:04:4D:A4:98:CA:2A:81",
    "A2": "00:07:04:4F:A4:98:CA:2A:81",
    "A3": "00:07:04:4E:A4:98:CA:2A:81",
    "A4": "00:07:04:47:A4:98:CA:2A:81",
    "B1": "00:07:04:3D:A4:98:CA:2A:81",
    "B2": "00:07:04:34:A4:98:CA:2A:81",
    "B3": "00:07:04:35:A4:98:CA:2A:81",
    "B4": "00:07:04:3E:A4:98:CA:2A:81",
    "C1": "00:07:04:44:A4:98:CA:2A:81",
    "C2": "00:07:04:36:A4:98:CA:2A:81",
    "C3": "00:07:04:45:A4:98:CA:2A:81",
    "C4": "00:07:04:3B:A4:98:CA:2A:81",
    "D1": "00:07:04:46:A4:98:CA:2A:81",
    "D2": "00:07:04:3C:A4:98:CA:2A:81",
    "D3": "00:07:04:2B:A4:98:CA:2A:81",
    "D4": "00:07:04:2A:A4:98:CA:2A:81",
    "HIVE": "00:07:04:2C:A4:98:CA:2A:81",
}

hive_uid = token_uids["HIVE"]


def _build_map(flowers):
    """Expand a coordinate-authored window into the UID-keyed map game.py needs.

    `flowers` maps each grid coordinate to (name, colour, next_coordinate),
    where next_coordinate is the deliver target (same flower type, different
    colour). Returns a dict keyed by real token UID, since that is what the
    scanner reports at runtime.
    """
    return {
        token_uids[coord]: {
            "name": name,
            "colour": colour,
            "coordinate": coord,
            "next_uid": token_uids[next_coord],
        }
        for coord, (name, colour, next_coord) in flowers.items()
    }


flower_map_morning = _build_map({
    "A1": ("Tulip",    "Red",    "B2"),
    "A2": ("Daisy",    "Blue",   "B1"),
    "A3": ("Poppy",    "Yellow", "B4"),
    "A4": ("Bluebell", "Orange", "B3"),
    "B1": ("Daisy",    "Yellow", "C4"),
    "B2": ("Tulip",    "Orange", "C3"),
    "B3": ("Bluebell", "Red",    "C2"),
    "B4": ("Poppy",    "Blue",   "C1"),
    "C1": ("Poppy",    "Orange", "D2"),
    "C2": ("Bluebell", "Yellow", "D1"),
    "C3": ("Tulip",    "Blue",   "D4"),
    "C4": ("Daisy",    "Red",    "D3"),
    "D1": ("Bluebell", "Blue",   "A4"),
    "D2": ("Poppy",    "Red",    "A3"),
    "D3": ("Daisy",    "Orange", "A2"),
    "D4": ("Tulip",    "Yellow", "A1"),
})

flower_map_midday = _build_map({
    "A1": ("Sunflower", "Blue",   "B2"),
    "A2": ("Marigold",  "Orange", "B1"),
    "A3": ("Rose",      "Red",    "B4"),
    "A4": ("Lavender",  "Yellow", "B3"),
    "B1": ("Marigold",  "Red",    "C4"),
    "B2": ("Sunflower", "Yellow", "C3"),
    "B3": ("Lavender",  "Blue",   "C2"),
    "B4": ("Rose",      "Orange", "C1"),
    "C1": ("Rose",      "Yellow", "D2"),
    "C2": ("Lavender",  "Red",    "D1"),
    "C3": ("Sunflower", "Orange", "D4"),
    "C4": ("Marigold",  "Blue",   "D3"),
    "D1": ("Lavender",  "Orange", "A4"),
    "D2": ("Rose",      "Blue",   "A3"),
    "D3": ("Marigold",  "Yellow", "A2"),
    "D4": ("Sunflower", "Red",    "A1"),
})

flower_map_afternoon = _build_map({
    "A1": ("Dahlia",    "Orange", "B2"),
    "A2": ("Foxglove",  "Red",    "B1"),
    "A3": ("Buttercup", "Yellow", "B4"),
    "A4": ("Clover",    "Blue",   "B3"),
    "B1": ("Foxglove",  "Yellow", "C4"),
    "B2": ("Dahlia",    "Blue",   "C3"),
    "B3": ("Clover",    "Orange", "C2"),
    "B4": ("Buttercup", "Red",    "C1"),
    "C1": ("Buttercup", "Blue",   "D2"),
    "C2": ("Clover",    "Yellow", "D1"),
    "C3": ("Dahlia",    "Red",    "D4"),
    "C4": ("Foxglove",  "Orange", "D3"),
    "D1": ("Clover",    "Red",    "A4"),
    "D2": ("Buttercup", "Orange", "A3"),
    "D3": ("Foxglove",  "Blue",   "A2"),
    "D4": ("Dahlia",    "Yellow", "A1"),
})

# Each window has its own flower set and petal->button encoding.
# petal_encoding[flower_name][petal_count] -> button colour to press.
# petal_count is randomly generated 1-4 at each flower scan.
bloom_windows = [
    {
        "name": "Morning",
        "start_seconds": 0,
        "map": flower_map_morning,
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
            "Dahlia":    {1: "Blue",   2: "Yellow", 3: "Green",  4: "Red"},
            "Foxglove":  {1: "Yellow", 2: "Green",  3: "Red",    4: "Blue"},
            "Buttercup": {1: "Green",  2: "Red",    3: "Blue",   4: "Yellow"},
            "Clover":    {1: "Red",    2: "Blue",   3: "Yellow", 4: "Green"},
        },
    },
]

game_duration_seconds = 600  # 10 minutes total
