class Level:
    """The level played"""

    def __init__(self, grid: list[list[int]]) -> None:
        """Build pacgums and spawn points from the maze grid."""
        self.grid = grid
        h = len(grid)
        w = len(grid[0])
        self.super_pacgums: set[tuple[int, int]] = {(0, 0), (w-1, 0),
                                                    (0, h-1), (w-1, h-1)}
        self.pacgums: set[tuple[int, int]] = set()
        for y in range(0, h):
            for x in range(0, w):
                coord = (x, y)
                if coord not in self.super_pacgums and grid[y][x] != 15:
                    self.pacgums.add(coord)
        x = w // 2
        y = h // 2
        while grid[y][x] == 15:
            x += 1
        self.player_spawn = (x, y)
        self.ghost_spawns: list[tuple[int, int]] = [(0, 0), (w-1, 0),
                                                    (0, h-1), (w-1, h-1)]
