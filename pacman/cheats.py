class Cheat:
    """Hold the cheat mode switches used to ease peer review."""
    def __init__(self) -> None:
        """Start with cheat mode and every cheat turned off."""
        self.invincible = False
        self.freeze = False
        self.always_edible = False
        self.speed_boost = False
        self.cheat_enabled = False

    def toggle_invincible(self) -> None:
        """Turn invincibility on or off (ghosts cannot kill Pac-Man)."""
        self.invincible = not self.invincible

    def toggle_freeze(self) -> None:
        """Turn ghost freeze on or off (ghosts and timer stop)."""
        self.freeze = not self.freeze

    def toggle_always_edible(self) -> None:
        """Turn on or off the cheat that keeps ghosts edible."""
        self.always_edible = not self.always_edible

    def toggle_speed_boost(self) -> None:
        """Turn on or off the cheat that changes Pac-man speed."""
        self.speed_boost = not self.speed_boost

    def toggle_cheat(self) -> None:
        """Switch cheat mode on or off and reset every cheat."""
        self.cheat_enabled = not self.cheat_enabled
        self.always_edible = False
        self.freeze = False
        self.invincible = False
