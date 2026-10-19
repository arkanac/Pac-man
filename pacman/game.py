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
        self.player.move()
        coord = self.player.position()
        if coord in self.level.pacgums:
            self.level.pacgums.discard(coord)
            self.score += self.rules.point_per_pacgum
