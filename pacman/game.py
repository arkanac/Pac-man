from pacman.entities import Player, Ghost, GhostState
from pacman.config import GameConfig
from pacman.ghost_ai import create_ghost
from pacman.level import build_level


class Game:
    """Apply the game rules: move the player, eat pacgums, keep the score."""

    def __init__(self, config: GameConfig) -> None:
        """Start a game on the given level with the given player and rules."""
        self.config = config
        self.rules = config.rules
        self.current_level = 1
        self.level = build_level(config, self.current_level)
        self.player = Player(*self.level.player_spawn, self.level.grid,
                             config.rules.lives)
        self.score: int = 0
        self.ghosts: list[Ghost] = create_ghost(self.level, self.player)
        self.current_level = 1

    def next_level(self) -> None:
        self.current_level += 1
        self.level = build_level(self.config, self.current_level)
        self.player.new_level(*self.level.player_spawn, self.level.grid)
        self.ghosts = create_ghost(self.level, self.player)

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
