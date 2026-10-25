from pacman.entities import Player, Ghost, GhostState
from pacman.level import Level
from pacman.config import Rules
from pacman.ghost_ai import create_ghost


class Game:
    """Apply the game rules: move the player, eat pacgums, keep the score."""

    def __init__(self, level: Level, player: Player, rules: Rules) -> None:
        """Start a game on the given level with the given player and rules."""
        self.player = player
        self.level = level
        self.score: int = 0
        self.rules = rules
        self.ghosts: list[Ghost] = create_ghost(level, player)

    def turn(self) -> None:
        """Move the player one step and eat what is on its cell."""
        self.player.move()
        coord = self.player.position()
        if coord in self.level.pacgums:
            self.level.pacgums.discard(coord)
            self.score += self.rules.point_per_pacgum
        elif coord in self.level.super_pacgums:
            self.level.super_pacgums.discard(coord)
            for ghost in self.ghosts:
                ghost.frighten(10)
            self.score += self.rules.point_per_super_pacgum
        self.check_collision()
        for ghost in self.ghosts:
            if not self.player.is_dead():
                ghost.move()
                self.check_collision()

    def check_collision(self) -> None:
        p_pos = self.player.position()
        for ghost in self.ghosts:
            g_pos = ghost.position()
            if p_pos == g_pos:
                if ghost.state == GhostState.NORMAL:
                    self.player.lose_life()
                    for gh in self.ghosts:
                        gh.respawn()
                    return
                elif ghost.state == GhostState.EDIBLE:
                    self.score += self.rules.point_per_ghost
                    ghost.state = GhostState.EATEN

    def win(self) -> bool:
        """Return True when no pacgum nor super-pacgum is left."""
        p = len(self.level.pacgums)
        sp = len(self.level.super_pacgums)
        return p == 0 and sp == 0
