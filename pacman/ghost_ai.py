from entities import Player, Ghost
from pacman.maze import find_short_path, Direction


class Blinky(Ghost):
    def target(self) -> tuple[int, int]:
        return (self.player.x, self.player.y)

    def choose_direction(self, free: list[Direction],
                         target_cell: tuple[int, int]) -> Direction:
        tx, ty = target_cell
        result = find_short_path(self.x, self.y, tx, ty, self.grid)
        if result is None or result not in free:
            return super().choose_direction(free, target_cell)
        return result


class Pinky(Ghost):
    def target(self) -> tuple[int, int]:
        if self.player.current_direction is None:
            return (self.player.x, self.player.y)
        px = self.player.x
        py = self.player.y
        dx, dy = self.player.current_direction.value
        return (px + 4*dx, py + 4*dy)


class Inky(Ghost):
    def __init__(self, x: int, y: int, grid: list[list[int]],
                 player: Player, blinky: Blinky) -> None:
        super().__init__(x, y, grid, player)
        self.blinky = blinky

    def target(self) -> tuple[int, int]:
        if self.player.current_direction is None:
            return (self.player.x, self.player.y)
        px = self.player.x
        py = self.player.y
        dx, dy = self.player.current_direction.value
        p_x = px + 2 * dx
        p_y = py + 2 * dy
        bx = self.blinky.x
        by = self.blinky.y
        return (2*p_x - bx, 2*p_y - by)


class Clyde(Ghost):
    def target(self) -> tuple[int, int]:
        px = self.player.x
        py = self.player.y
        distance = (self.x - px) ** 2 + (self.y - py) ** 2
        if distance > 64:
            return (px, py)
        return (self.spawn_x, self.spawn_y)
