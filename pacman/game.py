from pacman.entities import Player
from pacman.level import Level
from pacman.config import Rules


class Game:
    """Apply the game rules: move the player, eat pacgums, keep the score."""

    def __init__(self, level: Level, player: Player, rules: Rules) -> None:
        """Start a game on the given level with the given player and rules."""
        self.player = player
        self.level = level
        self.score: int = 0
        self.rules = rules

    def turn(self) -> None:
        """Move the player one step and eat what is on its cell."""
        self.player.move()
        coord = self.player.position()
        if coord in self.level.pacgums:
            self.level.pacgums.discard(coord)
            self.score += self.rules.point_per_pacgum
        elif coord in self.level.super_pacgums:
            self.level.super_pacgums.discard(coord)
            self.score += self.rules.point_per_super_pacgum

    def win(self) -> bool:
        """Return True when no pacgum nor super-pacgum is left."""
        p = len(self.level.pacgums)
        sp = len(self.level.super_pacgums)
        return p == 0 and sp == 0
