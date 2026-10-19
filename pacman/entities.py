from pacman.maze import Direction, try_move, free_direction


class Player:
    """The player controlled Pac-man"""

    def __init__(self, x: int, y: int, grid: list[list[int]], lives: int
                 ) -> None:
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.current_direction: Direction | None = None
        self.next_direction: Direction | None = None
        self.grid = grid
        self.lives = lives
        self.max_lives = lives

    def new_level(self, x: int, y: int, grid: list[list[int]]) -> None:
        self.grid = grid
        self.spawn_x = x
        self.spawn_y = y
        self.respawn()

    def set_direction(self, direction: Direction) -> None:
        """Set the direction of pac-man"""
        self.next_direction = direction

    def move(self) -> None:
        """Check if the wanted direction is possible and move to it"""
        if self.next_direction is not None:
            exits = free_direction(self.grid, self.x, self.y)
            if exits[self.next_direction]:
                self.current_direction = self.next_direction
        if self.current_direction is not None:
            self.x, self.y = try_move(self.grid, self.x, self.y,
                                      self.current_direction)

    def reset(self) -> None:
        """Reset after a game over"""
        self.lives = self.max_lives
        self.respawn()

    def respawn(self) -> None:
        """Respawn after a death"""
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.current_direction = None
        self.next_direction = None

    def lose_life(self) -> None:
        """Remove one life (never below zero) and respawn."""
        if self.lives > 0:
            self.lives -= 1
        self.respawn()

    def is_dead(self) -> bool:
        """Return True when the player has no life left."""
        return self.lives <= 0
