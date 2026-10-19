from enum import Enum


class Direction(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)


def free_direction(grid: list[list[int]], x: int, y: int
                   ) -> dict[Direction, bool]:
    """Return, for each direction, True if there is no wall on that side."""
    cell = grid[y][x]
    return {
        Direction.N: cell & 1 == 0,
        Direction.E: cell & 2 == 0,
        Direction.S: cell & 4 == 0,
        Direction.W: cell & 8 == 0,
    }


def try_move(grid: list[list[int]], x: int, y: int, direction: Direction
             ) -> tuple[int, int]:
    exits = free_direction(grid, x, y)
    if exits[direction]:
        dx, dy = direction.value
        return (x + dx, y + dy)
    else:
        return (x, y)
