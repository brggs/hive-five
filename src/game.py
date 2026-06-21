"""Bee Challenge game state machine.

Pure logic with no hardware dependencies (imports only `random`), so it runs
and is unit-testable on desktop CPython as well as MicroPython on the Badger.

The game loop (main.py) drives this class:
  - feed scans/presses via on_hive_scan / on_flower_scan / on_button
  - call tick(now) every iteration to advance time-based transitions
  - render the current screen from view()

All times are passed in as seconds (a monotonic float). Randomness is injected
via `rng` so tests can make it deterministic; it must provide randint() and
choice() like the stdlib `random` module.

State machine (see docs/design.md):

  IDLE -> WAITING_FOR_HIVE_SCAN
            -> SHOWING_COLLECT_TARGET -> SHOWING_COLLECT_INFO -> POLLEN_COLLECTED
            -> SHOWING_DELIVER_TARGET -> SHOWING_DELIVER_INFO -> POLLEN_DELIVERED
            -> WAITING_FOR_HIVE_SCAN

  wrong flower -> VENUS_FLY_TRAP, wrong button -> SPIDER (both: Eaten++, reset turn)
  timer expiry (any state) -> GAME_OVER
"""

try:
    import random as _random
except ImportError:  # pragma: no cover
    _random = None

# States
IDLE = "IDLE"
WAITING_FOR_HIVE_SCAN = "WAITING_FOR_HIVE_SCAN"
SHOWING_COLLECT_TARGET = "SHOWING_COLLECT_TARGET"
SHOWING_COLLECT_INFO = "SHOWING_COLLECT_INFO"
POLLEN_COLLECTED = "POLLEN_COLLECTED"
SHOWING_DELIVER_TARGET = "SHOWING_DELIVER_TARGET"
SHOWING_DELIVER_INFO = "SHOWING_DELIVER_INFO"
POLLEN_DELIVERED = "POLLEN_DELIVERED"
SPIDER = "SPIDER"
VENUS_FLY_TRAP = "VENUS_FLY_TRAP"
GAME_OVER = "GAME_OVER"

# How long the transient success/failure screens stay up (seconds).
SUCCESS_DWELL_SECONDS = 3.0
FAILURE_DWELL_SECONDS = 5.0


class Game:
    def __init__(self, bloom_windows, hive_uid, duration_seconds, rng=None):
        self.bloom_windows = bloom_windows
        self.hive_uid = hive_uid
        self.duration_seconds = duration_seconds
        self.rng = rng if rng is not None else _random

        self.state = IDLE
        self.pollinated = 0
        self.eaten = 0
        self.start_time = 0.0

        # Per-turn data, captured at hive scan so a turn finishes on the map it
        # began with even if the bloom window changes mid-turn.
        self.turn_window = None
        self.collect_uid = None
        self.deliver_uid = None

        # Set when a flower is scanned successfully.
        self.petal_count = None
        self.correct_button = None

        # Deadline for transient screens (POLLEN_*/SPIDER/VENUS); None otherwise.
        self._dwell_until = None

        # Shuffled sequence of flower type names for the active bloom window.
        # Rebuilt when the window changes or when all 4 types have been used.
        self._type_sequence = []
        self._sequence_window_name = None

    # -- lifecycle ---------------------------------------------------------

    def start(self):
        """Reset state and wait for the first Hive scan to start the clock."""
        self.start_time = None
        self.state = WAITING_FOR_HIVE_SCAN
        self._dwell_until = None

    def elapsed(self, now):
        if self.start_time is None:
            return 0.0
        return now - self.start_time

    def current_window(self, now):
        """The bloom window active at `now` (latest one whose start has passed)."""
        elapsed = self.elapsed(now)
        active = self.bloom_windows[0]
        for window in self.bloom_windows:
            if elapsed >= window["start_seconds"]:
                active = window
        return active

    # -- inputs ------------------------------------------------------------

    def on_hive_scan(self, now):
        if self.state != WAITING_FOR_HIVE_SCAN:
            return
        if self.start_time is None:
            self.start_time = now
        self.turn_window = self.current_window(now)
        self.collect_uid = self._next_collect_uid(self.turn_window)
        self.petal_count = None
        self.correct_button = None
        self.state = SHOWING_COLLECT_TARGET

    def on_flower_scan(self, uid, now):
        if self.state == SHOWING_COLLECT_TARGET:
            target, info_state = self.collect_uid, SHOWING_COLLECT_INFO
        elif self.state == SHOWING_DELIVER_TARGET:
            target, info_state = self.deliver_uid, SHOWING_DELIVER_INFO
        else:
            return  # scans only matter while a target is showing

        if uid == target:
            flower = self.turn_window["map"][uid]
            self.petal_count = self.rng.randint(1, 4)
            self.correct_button = self.turn_window["petal_encoding"][flower["name"]][self.petal_count]
            if self.state == SHOWING_COLLECT_TARGET:
                flower_map = self.turn_window["map"]
                candidates = [u for u, f in flower_map.items()
                              if f["name"] == flower["name"] and u != uid]
                self.deliver_uid = self.rng.choice(candidates)
            self.state = info_state
        elif uid in self.turn_window["map"]:
            self._fail(VENUS_FLY_TRAP, now)  # wrong flower
        # else: Hive token or unknown UID -> ignored, no penalty

    def on_button(self, colour, now):
        if self.state == SHOWING_COLLECT_INFO:
            if colour == self.correct_button:
                self.state = POLLEN_COLLECTED
                self._dwell_until = now + SUCCESS_DWELL_SECONDS
            else:
                self._fail(SPIDER, now)
        elif self.state == SHOWING_DELIVER_INFO:
            if colour == self.correct_button:
                self.pollinated += 1
                self.state = POLLEN_DELIVERED
                self._dwell_until = now + SUCCESS_DWELL_SECONDS
            else:
                self._fail(SPIDER, now)
        # else: button presses ignored outside the info screens

    def tick(self, now):
        """Advance time-based transitions. Call every loop iteration."""
        if self.state == GAME_OVER:
            return
        if self.elapsed(now) >= self.duration_seconds:
            self.state = GAME_OVER
            self._dwell_until = None
            return
        if self._dwell_until is not None and now >= self._dwell_until:
            self._dwell_until = None
            if self.state == POLLEN_COLLECTED:
                self.state = SHOWING_DELIVER_TARGET
            else:  # POLLEN_DELIVERED, SPIDER, VENUS_FLY_TRAP
                self.state = WAITING_FOR_HIVE_SCAN

    # -- helpers -----------------------------------------------------------

    def _fail(self, failure_state, now):
        self.eaten += 1
        self.collect_uid = None
        self.deliver_uid = None
        self.petal_count = None
        self.correct_button = None
        self.state = failure_state
        self._dwell_until = now + FAILURE_DWELL_SECONDS

    def _next_collect_uid(self, window):
        if window["name"] != self._sequence_window_name or not self._type_sequence:
            seen = []
            for flower in window["map"].values():
                if flower["name"] not in seen:
                    seen.append(flower["name"])
            remaining = list(seen)
            shuffled = []
            while remaining:
                chosen = self.rng.choice(remaining)
                shuffled.append(chosen)
                remaining.remove(chosen)
            self._type_sequence = shuffled
            self._sequence_window_name = window["name"]
        type_name = self._type_sequence.pop(0)
        candidates = [uid for uid, f in window["map"].items() if f["name"] == type_name]
        return self.rng.choice(candidates)

    def _flower_label(self, uid):
        flower = self.turn_window["map"][uid]
        return flower["colour"] + " " + flower["name"]

    def view(self):
        """A flat dict describing the current screen for the renderer."""
        v = {"state": self.state, "pollinated": self.pollinated, "eaten": self.eaten}
        if self.turn_window is not None:
            v["window"] = self.turn_window["name"]
        if self.state == SHOWING_COLLECT_TARGET:
            v["verb"] = "COLLECT FROM"
            v["flower"] = self._flower_label(self.collect_uid)
        elif self.state == SHOWING_DELIVER_TARGET:
            v["verb"] = "DELIVER TO"
            v["flower"] = self._flower_label(self.deliver_uid)
        elif self.state == SHOWING_COLLECT_INFO:
            v["flower"] = self._flower_label(self.collect_uid)
            v["petals"] = self.petal_count
        elif self.state == SHOWING_DELIVER_INFO:
            v["flower"] = self._flower_label(self.deliver_uid)
            v["petals"] = self.petal_count
        return v
