from pacman.entities import Player, Ghost, GhostState
from pacman.config import GameConfig
from pacman.ghost_ai import create_ghost
from pacman.level import build_level
from pacman.cheats import Cheat

TURN_PER_SECOND = 8
FRIGHTEN_TURN = 6 * TURN_PER_SECOND
MIN_LEVELS = 10


class Game:
    """Run a Pac-Man game: levels, player, ghosts, score and timer."""

    def __init__(self, config: GameConfig) -> None:
        """Build level 1, the player and the ghosts from the config."""
        self.config = config
        self.rules = config.rules
        self.current_level = 1
        self.level = build_level(config, self.current_level)
        self.player = Player(*self.level.player_spawn, self.level.grid,
                             config.rules.lives)
        self.score: int = 0
        self.ghosts: list[Ghost] = create_ghost(self.level, self.player)
        self.total_levels = max(MIN_LEVELS, len(self.config.game_specs))
        self.time_left = self.level.max_time * TURN_PER_SECOND
        self.cheats = Cheat()

    def next_level(self) -> None:
        """Load the next level and reset the timer, player and ghosts."""
        self.current_level += 1
        self.level = build_level(self.config, self.current_level)
        self.time_left = self.level.max_time * TURN_PER_SECOND
        self.player.new_level(*self.level.player_spawn, self.level.grid)
        self.ghosts = create_ghost(self.level, self.player)

    def turn(self) -> None:
        """Play one turn: move, eat, move ghosts, check collisions, tick."""
        if self.cheats.always_edible:
            for ghost in self.ghosts:
                ghost.frighten(FRIGHTEN_TURN)
        self.player.move()
        coord = self.player.position()
        if coord in self.level.pacgums:
            self.level.pacgums.discard(coord)
            self.score += self.rules.point_per_pacgum
        elif coord in self.level.super_pacgums:
            self.level.super_pacgums.discard(coord)
            for ghost in self.ghosts:
                ghost.frighten(FRIGHTEN_TURN)
            self.score += self.rules.point_per_super_pacgum
        self.check_collision()
        for ghost in self.ghosts:
            if not self.player.is_dead():
                if not self.cheats.freeze:
                    ghost.move()
                self.check_collision()
        if not self.cheats.freeze:
            self.time_left -= 1

    def check_collision(self) -> None:
        """Resolve Pac-Man / ghost collisions according to ghost state."""
        p_pos = self.player.position()
        for ghost in self.ghosts:
            g_pos = ghost.position()
            if p_pos == g_pos:
                if ghost.state == GhostState.NORMAL:
                    if self.cheats.invincible:
                        continue
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

    def is_last_level(self) -> bool:
        """Return True if the current level is the last one."""
        return self.current_level >= self.total_levels

    def time_up(self) -> bool:
        """Return True when the level timer has run out."""
        return self.time_left <= 0
