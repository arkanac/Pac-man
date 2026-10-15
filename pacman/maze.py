def free_direction(grid: list[list[int]], x: int, y: int) -> dict[str, bool]:
    """Return, for each direction, True if there is no wall on that side."""
    cell = grid[y][x]
    return {
        "N": cell & 1 == 0,
        "E": cell & 2 == 0,
        "S": cell & 4 == 0,
        "W": cell & 8 == 0,
    }
