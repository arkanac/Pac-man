from enum import Enum
from collections import deque

Cell = tuple[int, int]


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


def find_short_path(x: int, y: int, gx: int, gy: int,
                    grid: list[list[int]]) -> Direction | None:
    start = (x, y)
    goal = (gx, gy)
    if start == goal:
        return None
    prev: dict[Cell, tuple[Cell, Direction] | None] = {start: None}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            break
        for direction, possible in free_direction(grid, x, y).items():
            dx, dy = direction.value
            nx, ny = x + dx, y + dy
            if possible and (nx, ny) not in prev:
                prev[(nx, ny)] = ((x, y), direction)
                queue.append((nx, ny))
    if goal not in prev:
        return None
    path: list[Direction] = []
    cur = goal
    while True:
        step = prev[cur]
        if step is None:
            break
        parent, direction = step
        path.append(direction)
        cur = parent
    return path[-1]
