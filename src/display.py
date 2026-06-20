import badger2040

# e-ink panel is 296 x 128 px.
WIDTH = 296
HEIGHT = 128
SCORE_Y = 112  # baseline-ish for the persistent footer


class Display:
    def __init__(self):
        self.d = badger2040.Badger2040()
        self.d.set_update_speed(badger2040.UPDATE_FAST)

    # -- low-level helpers -------------------------------------------------

    def _begin(self):
        self.d.set_pen(15)
        self.d.clear()
        self.d.set_pen(0)
        self.d.set_font("bitmap8")
        self.d.set_thickness(1)

    def _score_bar(self, pollinated, eaten):
        self.d.text(
            "Pollinated: {} | Eaten: {}".format(pollinated, eaten),
            6, SCORE_Y, scale=2,
        )

    def _screen(self, lines, pollinated, eaten):
        """Draw a stack of (text, y, scale) lines plus the score footer."""
        self._begin()
        for text, y, scale in lines:
            self.d.text(text, 10, y, scale=scale)
        self._score_bar(pollinated, eaten)
        self.d.update()

    # -- generic messages (used for boot / errors) -------------------------

    def show_message(self, title, body):
        self._begin()
        self.d.set_thickness(2)
        self.d.text(title, 10, 20, scale=3)
        self.d.set_thickness(1)
        self.d.text(body, 10, 70, scale=2)
        self.d.update()

    # -- game screens ------------------------------------------------------

    def show_waiting(self, pollinated, eaten):
        self._screen([
            ("Hand the Bee to the", 14, 2),
            ("next player!", 38, 2),
            ("Scan the Hive to start.", 74, 2),
        ], pollinated, eaten)

    def show_target(self, verb, flower, window, pollinated, eaten):
        # verb is "COLLECT FROM" or "DELIVER TO"; window is the bloom window name.
        self._screen([
            ("{}  ({})".format(verb, window), 12, 2),
            (flower, 48, 3),
            ("Hive team: check the map!", 84, 2),
        ], pollinated, eaten)

    def show_info(self, flower, petals, window, pollinated, eaten):
        # window is the (frozen) bloom window for this turn, so the Hive team
        # reads the right petal->button table even when a turn straddles a
        # window boundary.
        self._screen([
            ("You found:  ({})".format(window), 12, 2),
            (flower, 40, 3),
            ("Petals: {}".format(petals), 72, 2),
            ("Shout name & petals!", 92, 2),
        ], pollinated, eaten)

    def show_collected(self, pollinated, eaten):
        self._screen([
            ("POLLEN COLLECTED!", 18, 3),
            ("Now deliver it to", 60, 2),
            ("another flower!", 82, 2),
        ], pollinated, eaten)

    def show_delivered(self, pollinated, eaten):
        self._screen([
            ("POLLINATED!", 18, 3),
            ("Return to the Hive and", 60, 2),
            ("hand over the Bee.", 82, 2),
        ], pollinated, eaten)

    def show_spider(self, pollinated, eaten):
        self._screen([
            ("EATEN BY A SPIDER!", 18, 3),
            ("(wrong button)", 52, 2),
            ("Return to the Hive.", 82, 2),
        ], pollinated, eaten)

    def show_venus(self, pollinated, eaten):
        self._screen([
            ("VENUS FLY TRAP!", 18, 3),
            ("(wrong flower)", 52, 2),
            ("Return to the Hive.", 82, 2),
        ], pollinated, eaten)

    def show_game_over(self, pollinated, eaten):
        self._begin()
        self.d.set_thickness(2)
        self.d.text("GAME OVER", 10, 18, scale=3)
        self.d.set_thickness(1)
        self.d.text("Flowers pollinated: {}".format(pollinated), 10, 56, scale=2)
        self.d.text("Bees eaten: {}".format(eaten), 10, 80, scale=2)
        self.d.text("Well done everyone!", 10, 100, scale=2)
        self.d.text("Green+Yellow to restart", 10, 116, scale=1)
        self.d.update()
