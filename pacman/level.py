import random
from pacman.config import GameConfig
from mazegenerator import MazeGenerator



class Level:
    """A maze with its pacgums, super-pacgums, spawns and time limit."""

    def __init__(self, grid: list[list[int]], max_time: int) -> None:
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
        self.pacgums.discard((x, y))
        self.ghost_spawns: list[tuple[int, int]] = [(0, 0), (w-1, 0),
                                                    (0, h-1), (w-1, h-1)]
        self.max_time = max_time


def to_int_seed(seed: int | str) -> int:
    """Turn any int or str into a stable positive int seed."""
    if isinstance(seed, str):
        if seed.strip().isdigit():
            seed = int(seed)
        else:
            return random.Random(seed).randint(1, 2**31 - 1)
    if seed > 0:
        return seed
    return random.Random(seed).randint(1, 2**31 - 1)


def build_level(config: GameConfig, number: int) -> Level:
    """Generate level `number` from the config (fixed seed for level 1)."""
    index = min(number, len(config.game_specs)) - 1
    specs = config.game_specs[index]
    width = specs.width
    height = specs.height
    seed = to_int_seed(config.seed) if number == 1 else 0
    try:
        grid = MazeGenerator(size=(width, height), perfect=False, seed=seed)
    except Exception as e:
        raise ValueError(f"Maze generation failed for level {number}: "
                         f"{e}") from e
    return Level(grid.maze, specs.level_max_time)
