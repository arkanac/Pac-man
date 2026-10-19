import mlx_wrapper
from typing import Any
# from ..maze import Enum
import argparse


class Renderer():
    def __init__(self):
        self.height: int = 800
        self.width: int = 800
        self.image = None
        self.pixels: Any = None
        self.screen = None
        self.edge_size = 20
        self.edge_color: int = 0xFF0000

    def initialization(self) -> None:
        """Initialize the UI and the Window"""
        mlx_wrapper.initialisation()
        self.screen = mlx_wrapper.new_window(self.width, self.height)

    def create_image(self) -> None:
        """Put an image on the window, prepare the pixel to be written"""
        self.image = mlx_wrapper.new_image(self.width, self.height)
        self.pixels = mlx_wrapper.get_data_addr(self.image)

    def draw_line(self, start: tuple[int, int]) -> None:
        """Draw an horizontal line"""
        x_start, y_start = start
        x_end = x_start + self.edge_size
        x = x_start
        while (x != x_end):
            self.pixels[x, y_start] = self.edge_color
            x += 1

    def draw_column(self, start: tuple[int, int]) -> None:
        """Draw a vertical line"""
        x_start, y_start = start
        y_end = y_start - self.edge_size
        y = y_start
        while (y != y_end):
            self.pixels[x_start, y] = self.edge_color
            y -= 1

    def draw_cells(self, cell_value: int, cell_pos: tuple[int, int]) -> None:
        x_start, y_start = cell_pos
        if cell_value & 1:
            # draw top cell
            x0 = x_start
            y0 = y_start + self.edge_size
            self.draw_line((x0, y0))
        if cell_value & 2:
            # draw right cell
            x0 = x_start + self.edge_size
            y0 = y_start + self.edge_size
            self.draw_column((x0, y0))
        if cell_value & 4:
            # draw down cell
            x0 = x_start
            y0 = y_start
            self.draw_line((x0, y0))
        if cell_value & 8:
            # draw left cell
            x0 = x_start
            y0 = y_start + self.edge_size
            self.draw_column((x0, y0))

    def draw_maze(self, maze: list[list[int]]):
        for pos_y, line in enumerate(maze):
            for pos_x, cell in enumerate(line):
                cell_pos = pos_x * self.edge_size, pos_y * self.edge_size
                print(cell)
                # self.draw_cells(cell, cell_pos)
        mlx_wrapper.blit_img(self.image, self.screen, (0, 0))


parser = argparse.ArgumentParser()
parser.add_argument("maze_file", nargs="?", help="Path test lab")
args = parser.parse_args()
rend = Renderer()
rend.create_image()
with open(args.maze_file) as f:
    rend.draw_maze(f)
