import badger2040


class Display:
    def __init__(self):
        self.d = badger2040.Badger2040()
        self.d.set_update_speed(badger2040.UPDATE_FAST)

    def show_message(self, title, body):
        self.d.set_pen(15)
        self.d.clear()
        self.d.set_pen(0)
        self.d.set_font("bitmap8")
        self.d.set_thickness(2)
        self.d.text(title, 10, 20, scale=3)
        self.d.set_thickness(1)
        self.d.text(body,  10, 70, scale=2)
        self.d.update()

    def show_idle(self):
        self.d.set_pen(15)
        self.d.clear()
        self.d.set_pen(0)
        self.d.set_font("bitmap8")
        self.d.text("Waiting...",      10, 20, scale=2)
        self.d.text("Scan a tag or",   10, 55, scale=2)
        self.d.text("press a button",  10, 80, scale=2)
        self.d.update()
