


class Cheat:
    def __init__(self):
        self.invincible = False
        self.freeze = False
        self.always_edible = False

    def toggle_invincible(self) -> None:
        self.invincible = not self.invincible

    def toggle_freeze(self) -> None:
        self.freeze = not self.freeze

    def toggle_always_edible(self) -> None:
        self.always_edible = not self.always_edible
