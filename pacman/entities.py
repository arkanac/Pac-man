from pacman.maze import Direction, try_move, free_direction


class Player:
    """The player controlled Pac-man"""

    def __init__(self, x: int, y: int, grid: list[list[int]]) -> None:
        self.x = x
        self.y = y
        self.current_direction: Direction | None = None
        self.next_direction: Direction | None = None
        self.grid = grid

    def set_direction(self, direction: Direction) -> None:
        self.next_direction = direction

    def move(self) -> None:
        if self.next_direction is not None:
            exits = free_direction(self.grid, self.x, self.y)
            if exits[self.next_direction]:
                self.current_direction = self.next_direction
        if self.current_direction is not None:
            self.x, self.y = try_move(self.grid, self.x, self.y,
                                      self.current_direction)
