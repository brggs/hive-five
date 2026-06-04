"""Bee Challenge game data.

Authoritative spec: docs/flower-maps.md and docs/design.md.

The 16 physical RFID tokens never move; each bloom window remaps them to a
different set of flower identities. Replace the UID_XX placeholders with the
real scanned token UIDs before playing on hardware. UIDs are the hex strings
returned by PN532.read_passive_target(), e.g. "04:A2:1B:5C".

The button to press is NOT stored per flower. It is resolved at scan time from
petal_encoding[flower_name][petal_count], where petal_count is a random integer
1-4 generated each time a flower is scanned.
"""

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
    "UID_A1": {"name": "Dahlia",    "colour": "Yellow", "coordinate": "A1", "next_uid": "UID_B1"},
    "UID_A2": {"name": "Foxglove",  "colour": "Yellow", "coordinate": "A2", "next_uid": "UID_B2"},
    "UID_A3": {"name": "Buttercup", "colour": "Yellow", "coordinate": "A3", "next_uid": "UID_B3"},
    "UID_A4": {"name": "Clover",    "colour": "Yellow", "coordinate": "A4", "next_uid": "UID_B4"},
    "UID_B1": {"name": "Dahlia",    "colour": "Red",    "coordinate": "B1", "next_uid": "UID_C1"},
    "UID_B2": {"name": "Foxglove",  "colour": "Red",    "coordinate": "B2", "next_uid": "UID_C2"},
    "UID_B3": {"name": "Buttercup", "colour": "Red",    "coordinate": "B3", "next_uid": "UID_C3"},
    "UID_B4": {"name": "Clover",    "colour": "Red",    "coordinate": "B4", "next_uid": "UID_C4"},
    "UID_C1": {"name": "Dahlia",    "colour": "Green",  "coordinate": "C1", "next_uid": "UID_D1"},
    "UID_C2": {"name": "Foxglove",  "colour": "Green",  "coordinate": "C2", "next_uid": "UID_D2"},
    "UID_C3": {"name": "Buttercup", "colour": "Green",  "coordinate": "C3", "next_uid": "UID_D3"},
    "UID_C4": {"name": "Clover",    "colour": "Green",  "coordinate": "C4", "next_uid": "UID_D4"},
    "UID_D1": {"name": "Dahlia",    "colour": "Blue",   "coordinate": "D1", "next_uid": "UID_A1"},
    "UID_D2": {"name": "Foxglove",  "colour": "Blue",   "coordinate": "D2", "next_uid": "UID_A2"},
    "UID_D3": {"name": "Buttercup", "colour": "Blue",   "coordinate": "D3", "next_uid": "UID_A3"},
    "UID_D4": {"name": "Clover",    "colour": "Blue",   "coordinate": "D4", "next_uid": "UID_A4"},
}

hive_uid = "UID_HIVE"

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
