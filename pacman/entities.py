from pacman.maze import Direction, try_move, free_direction, find_short_path
from abc import ABC, abstractmethod
from enum import Enum


class GhostState(Enum):
    """The three possible states of a ghost."""

    NORMAL = 1
    EDIBLE = 2
    EATEN = 3


class Entity(ABC):
    """Common base for everything that moves on the grid."""

    def __init__(self, x: int, y: int, grid: list[list[int]]) -> None:
        """Place the entity on its spawn cell of the given grid."""
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.current_direction: Direction | None = None
        self.grid = grid

    def new_level(self, x: int, y: int, grid: list[list[int]]) -> None:
        """Move the entity to a new grid with a new spawn cell."""
        self.grid = grid
        self.spawn_x = x
        self.spawn_y = y
        self.respawn()

    @abstractmethod
    def move(self) -> None:
        """Move the entity by one cell."""
        pass

    def respawn(self) -> None:
        """Put the entity back on its spawn cell, with no direction."""
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.current_direction = None

    def position(self) -> tuple[int, int]:
        """Return the current (x, y) cell."""
        return (self.x, self.y)


class Player(Entity):
    """The player-controlled Pac-Man."""

    def __init__(self, x: int, y: int, grid: list[list[int]], lives: int
                 ) -> None:
        """Create Pac-Man on its spawn cell with the given lives."""
        super().__init__(x, y, grid)
        self.next_direction: Direction | None = None
        self.lives = lives
        self.max_lives = lives

    def set_direction(self, direction: Direction) -> None:
        """Buffer the direction wanted by the player."""
        self.next_direction = direction

    def move(self) -> None:
        """Turn to the wanted direction if possible, then move one cell."""
        if self.next_direction is not None:
            exits = free_direction(self.grid, self.x, self.y)
            if exits[self.next_direction]:
                self.current_direction = self.next_direction
        if self.current_direction is not None:
            self.x, self.y = try_move(self.grid, self.x, self.y,
                                      self.current_direction)

    def reset(self) -> None:
        """Restore all lives and respawn, after a game over."""
        self.lives = self.max_lives
        self.respawn()

    def respawn(self) -> None:
        """Respawn after a death and forget the buffered direction."""
        super().respawn()
        self.next_direction = None

    def lose_life(self) -> None:
        """Remove one life (never below zero) and respawn."""
        if self.lives > 0:
            self.lives -= 1
        self.respawn()

    def add_life(self) -> None:
        """Cheat: give Pac-Man one extra life."""
        self.lives += 1

    def is_dead(self) -> bool:
        """Return True when the player has no life left."""
        return self.lives <= 0


class Ghost(Entity):
    """A ghost: chases, flees when edible, returns home when eaten."""

    def __init__(self, x: int, y: int, grid: list[list[int]],
                 player: Player) -> None:
        """Create a ghost on its corner, aware of the player."""
        super().__init__(x, y, grid)
        self.player = player
        self.state = GhostState.NORMAL
        self.count = 0

    def move(self) -> None:
        """Pick a direction according to the state and move one cell.

        Edible ghosts move one turn out of two (half speed).
        """
        exits = free_direction(self.grid, self.x, self.y)
        free = [direction for direction, possible in exits.items() if possible]
        self.block_opposite(free)
        if self.state is GhostState.EDIBLE:
            self.count -= 1
            if self.count <= 0:
                self.state = GhostState.NORMAL
            if self.count % 2 == 0 and self.state is GhostState.EDIBLE:
                return
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
        """Make the ghost edible for `duration` turns, unless it is eaten."""
        if self.state is GhostState.EATEN:
            return None
        self.count = duration
        self.state = GhostState.EDIBLE

    def block_opposite(self, possible_way: list[Direction]) -> None:
        """Remove the U-turn from the free directions, except in dead ends."""
        if self.current_direction is not None:
            x, y = self.current_direction.value
            (x, y) = (-x, -y)
            if len(possible_way) > 1:
                if Direction((x, y)) in possible_way:
                    possible_way.remove(Direction((x, y)))

    def choose_direction(self, free: list[Direction],
                         target_cell: tuple[int, int]) -> Direction:
        """Return the free direction closest (straight line) to the target."""
        tx, ty = target_cell

        def distance(direction: Direction) -> int:
            """Squared distance from the next cell to the target."""
            dx, dy = direction.value
            nx, ny = self.x + dx, self.y + dy
            return (nx - tx) ** 2 + (ny - ty) ** 2
        return min(free, key=distance)

    def fleeing(self) -> tuple[int, int]:
        """Return the flee target: Pac-Man mirrored around the ghost."""
        px = self.player.x
        py = self.player.y
        return (2 * self.x - px, 2 * self.y - py)

    def eaten(self, free: list[Direction]) -> Direction:
        """Return the next step home (BFS); back to NORMAL once arrived."""
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
        """Respawn on its corner as a NORMAL ghost."""
        super().respawn()
        self.count = 0
        self.state = GhostState.NORMAL

    @abstractmethod
    def target(self) -> tuple[int, int]:
        """Return the chase target cell, specific to each ghost."""
        pass
