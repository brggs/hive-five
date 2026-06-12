"""Desktop unit tests for the Bee Challenge game state machine.

Runs on plain CPython with no hardware and no real token UIDs:

    python3 src/tests.py

Randomness and the clock are both injected so every run is deterministic.
"""

import sys

import game
from game import Game
import game_data


def _uid_at(coordinate):
    """Real token UID for a grid coordinate, so tests don't hardcode hex UIDs."""
    for uid, flower in game_data.flower_map_morning.items():
        if flower["coordinate"] == coordinate:
            return uid
    raise KeyError(coordinate)


# Symbolic handles for the physical tokens used by the tests.
A1       = _uid_at("A1")                              # Morning: Red Tulip
A1_NEXT  = game_data.flower_map_morning[A1]["next_uid"]  # Morning: Orange Tulip — A1's deliver target
C3       = _uid_at("C3")                              # Morning: Blue Tulip (wrong flower, never the test target)
D2       = _uid_at("D2")                              # Morning: Red Poppy


class FakeRng:
    """Deterministic stand-in for the `random` module.

    choice() returns whatever `choice_value` is currently set to (ignoring the
    sequence), and randint() returns `randint_value`.
    """

    def __init__(self, choice_value=A1, randint_value=1):
        self.choice_value = choice_value
        self.randint_value = randint_value

    def choice(self, seq):
        return self.choice_value

    def randint(self, a, b):
        return self.randint_value


def new_game(rng):
    g = Game(
        game_data.bloom_windows,
        game_data.hive_uid,
        game_data.game_duration_seconds,
        rng=rng,
    )
    g.start(0.0)
    return g


# -- tiny assert framework -------------------------------------------------

_failures = []


def check(cond, msg):
    if not cond:
        _failures.append(msg)
        print("  FAIL:", msg)
    else:
        print("  ok:", msg)


# -- tests -----------------------------------------------------------------

def test_happy_path():
    print("test_happy_path")
    rng = FakeRng(choice_value=A1, randint_value=1)  # Red Tulip, petals=1 -> Red
    g = new_game(rng)

    g.on_hive_scan(0.0)
    check(g.state == game.SHOWING_COLLECT_TARGET, "hive scan shows collect target")
    check(g.collect_uid == A1, "collect target is the chosen flower")
    check(g.deliver_uid == A1_NEXT, "deliver target is next_uid (same type, diff colour)")

    g.on_flower_scan(A1, 1.0)
    check(g.state == game.SHOWING_COLLECT_INFO, "correct collect flower -> info")
    check(g.correct_button == "Red", "Morning Tulip petals=1 resolves to Red")

    g.on_button("Red", 2.0)
    check(g.state == game.POLLEN_COLLECTED, "correct button -> pollen collected")
    g.tick(2.0 + game.SUCCESS_DWELL_SECONDS)
    check(g.state == game.SHOWING_DELIVER_TARGET, "after dwell -> deliver target")

    g.on_flower_scan(A1_NEXT, 6.0)
    check(g.state == game.SHOWING_DELIVER_INFO, "correct deliver flower -> info")

    g.on_button("Red", 7.0)
    check(g.state == game.POLLEN_DELIVERED, "correct button -> pollen delivered")
    check(g.pollinated == 1, "pollinated incremented on delivery")
    check(g.eaten == 0, "nothing eaten on a clean turn")
    g.tick(7.0 + game.SUCCESS_DWELL_SECONDS)
    check(g.state == game.WAITING_FOR_HIVE_SCAN, "after dwell -> waiting for next player")


def test_wrong_button_spider():
    print("test_wrong_button_spider")
    rng = FakeRng(choice_value=A1, randint_value=1)  # correct = Red
    g = new_game(rng)
    g.on_hive_scan(0.0)
    g.on_flower_scan(A1, 1.0)

    g.on_button("Orange", 2.0)  # wrong
    check(g.state == game.SPIDER, "wrong button -> spider")
    check(g.eaten == 1, "spider increments eaten")
    check(g.pollinated == 0, "spider does not score")
    g.tick(2.0 + game.FAILURE_DWELL_SECONDS)
    check(g.state == game.WAITING_FOR_HIVE_SCAN, "spider resets to waiting")
    check(g.collect_uid is None, "turn data cleared on reset")


def test_wrong_flower_venus():
    print("test_wrong_flower_venus")
    rng = FakeRng(choice_value=A1)
    g = new_game(rng)
    g.on_hive_scan(0.0)

    g.on_flower_scan(C3, 1.0)  # a real flower, but not the target
    check(g.state == game.VENUS_FLY_TRAP, "wrong flower -> venus fly trap")
    check(g.eaten == 1, "venus increments eaten")
    g.tick(1.0 + game.FAILURE_DWELL_SECONDS)
    check(g.state == game.WAITING_FOR_HIVE_SCAN, "venus resets to waiting")


def test_unknown_and_hive_scans_ignored_midturn():
    print("test_unknown_and_hive_scans_ignored_midturn")
    rng = FakeRng(choice_value=A1)
    g = new_game(rng)
    g.on_hive_scan(0.0)

    g.on_flower_scan("NOT_A_TOKEN", 1.0)
    check(g.state == game.SHOWING_COLLECT_TARGET, "unknown UID ignored, no penalty")
    g.on_flower_scan(game_data.hive_uid, 1.5)
    check(g.state == game.SHOWING_COLLECT_TARGET, "hive token mid-turn ignored")
    check(g.eaten == 0, "no penalty from ignored scans")


def test_hive_rerandomises_target():
    print("test_hive_rerandomises_target")
    rng = FakeRng(choice_value=A1)
    g = new_game(rng)
    g.on_hive_scan(0.0)
    check(g.collect_uid == A1, "first target chosen")

    # Fail the turn, return to waiting, then a new target is drawn on next scan.
    g.on_flower_scan(C3, 1.0)
    g.tick(1.0 + game.FAILURE_DWELL_SECONDS)
    rng.choice_value = D2
    g.on_hive_scan(10.0)
    check(g.collect_uid == D2, "fresh random target after reset")


def test_bloom_window_boundary():
    print("test_bloom_window_boundary")
    rng = FakeRng(choice_value=A1, randint_value=1)
    g = new_game(rng)

    # Turn starts in the Morning window (t=0).
    g.on_hive_scan(0.0)
    check(g.turn_window["name"] == "Morning", "turn starts in Morning")

    # Time crosses into Midday (start 180s) mid-turn; the turn keeps its map.
    g.on_flower_scan(A1, 200.0)
    check(g.turn_window["name"] == "Morning", "in-progress turn stays on Morning map")
    check(g.correct_button == "Red", "uses Morning encoding (Tulip p1 = Red)")
    g.on_button("Red", 201.0)
    g.tick(201.0 + game.SUCCESS_DWELL_SECONDS)
    g.on_flower_scan(A1_NEXT, 205.0)
    g.on_button(g.correct_button, 206.0)
    g.tick(206.0 + game.SUCCESS_DWELL_SECONDS)
    check(g.state == game.WAITING_FOR_HIVE_SCAN, "turn completes")

    # Next turn (still t>=180) draws from the Midday map.
    g.on_hive_scan(210.0)
    check(g.turn_window["name"] == "Midday", "next turn uses Midday map")
    check(g.turn_window["map"][A1]["name"] == "Sunflower", "Midday remaps the token")


def test_timer_expiry_game_over():
    print("test_timer_expiry_game_over")
    rng = FakeRng(choice_value=A1)
    g = new_game(rng)
    g.on_hive_scan(0.0)
    g.tick(game_data.game_duration_seconds)  # exactly at expiry
    check(g.state == game.GAME_OVER, "timer expiry forces game over from any state")
    g.tick(game_data.game_duration_seconds + 100)
    check(g.state == game.GAME_OVER, "game over is terminal")


def main():
    tests = [
        test_happy_path,
        test_wrong_button_spider,
        test_wrong_flower_venus,
        test_unknown_and_hive_scans_ignored_midturn,
        test_hive_rerandomises_target,
        test_bloom_window_boundary,
        test_timer_expiry_game_over,
    ]
    for t in tests:
        t()
    print()
    if _failures:
        print("{} check(s) FAILED".format(len(_failures)))
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
