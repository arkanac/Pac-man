from pacman.maze import Direction, try_move, free_direction, find_short_path
from abc import ABC, abstractmethod
from enum import Enum


class GhostState(Enum):
    NORMAL = 1
    EDIBLE = 2
    EATEN = 3


class Entity(ABC):
    def __init__(self, x: int, y: int, grid: list[list[int]]) -> None:
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.current_direction: Direction | None = None
        self.grid = grid

    def new_level(self, x: int, y: int, grid: list[list[int]]) -> None:
        self.grid = grid
        self.spawn_x = x
        self.spawn_y = y
        self.respawn()

    @abstractmethod
    def move(self) -> None:
        pass

    def respawn(self) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.current_direction = None

    def position(self) -> tuple[int, int]:
        return (self.x, self.y)


class Player(Entity):
    """The player controlled Pac-man"""

    def __init__(self, x: int, y: int, grid: list[list[int]], lives: int
                 ) -> None:
        super().__init__(x, y, grid)
        self.next_direction: Direction | None = None
        self.lives = lives
        self.max_lives = lives

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
        super().respawn()
        self.next_direction = None

    def lose_life(self) -> None:
        """Remove one life (never below zero) and respawn."""
        if self.lives > 0:
            self.lives -= 1
        self.respawn()

    def is_dead(self) -> bool:
        """Return True when the player has no life left."""
        return self.lives <= 0


class Ghost(Entity):
    """The ghost chasing the player"""

    def __init__(self, x: int, y: int, grid: list[list[int]],
                 player: Player) -> None:
        super().__init__(x, y, grid)
        self.player = player
        self.state = GhostState.NORMAL
        self.count = 0

    def move(self) -> None:
        exits = free_direction(self.grid, self.x, self.y)
        free = [direction for direction, possible in exits.items() if possible]
        self.block_opposite(free)
        if self.state is GhostState.EDIBLE:
            self.count -= 1
            if self.count <= 0:
                self.state = GhostState.NORMAL
            self.current_direction = self.choose_direction(free,
                                                           self.fleeing())
        elif self.state is GhostState.EATEN:
            self.current_direction = self.eaten(free)
        else:
            target_cell = self.target()
            self.current_direction = self.choose_direction(free, target_cell)
        self.x, self.y = try_move(self.grid, self.x, self.y,
                                  self.current_direction)

    def frighten(self, duration: int) -> None:
        if self.state is GhostState.EATEN:
            return None
        self.count = duration
        self.state = GhostState.EDIBLE

    def block_opposite(self, possible_way: list[Direction]) -> None:
        if self.current_direction is not None:
            x, y = self.current_direction.value
            (x, y) = (-x, -y)
            if len(possible_way) > 1:
                if Direction((x, y)) in possible_way:
                    possible_way.remove(Direction((x, y)))

    def choose_direction(self, free: list[Direction],
                         target_cell: tuple[int, int]) -> Direction:
        tx, ty = target_cell

        def distance(direction: Direction) -> int:
            dx, dy = direction.value
            nx, ny = self.x + dx, self.y + dy
            return (nx - tx) ** 2 + (ny - ty) ** 2
        return min(free, key=distance)

    def fleeing(self) -> tuple[int, int]:
        px = self.player.x
        py = self.player.y
        return (2 * self.x - px, 2 * self.y - py)

    def eaten(self, free: list[Direction]) -> Direction:
        pos: tuple[int, int] = self.x, self.y
        spawn: tuple[int, int] = self.spawn_x, self.spawn_y
        if pos == spawn:
            self.state = GhostState.NORMAL
            target = self.target()
            return self.choose_direction(free, target)
        result = find_short_path(*pos, *spawn, self.grid)
        if result is None or result not in free:
            return self.choose_direction(free, spawn)
        return result

    def respawn(self) -> None:
        super().respawn()
        self.count = 0
        self.state = GhostState.NORMAL

    @abstractmethod
    def target(self) -> tuple[int, int]:
        pass
