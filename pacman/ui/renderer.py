import mlx_wrapper
from typing import Any
# from ..maze import Enum
import pygame
import sys
from mazegenerator import MazeGenerator


class Renderer():
    def __init__(self):
        """Useful variables for setting up the Visual Engine"""
        self.height: int = 800
        self.width: int = 600
        self.image = None
        self.pixels: Any = None
        self.screen = None
        self.x_padding = 500
        self.y_padding = 20

    def clip_rect(self, x0: int, x1: int, y0: int, y1: int):
        """Clip the bounding box to ensure no visual errors"""
        return (
            max(0, x0),
            min(self.width, x1),
            max(0, y0),
            min(self.height, y1)
            )

    def initialization(self) -> None:
        """Initialize the UI and the Window"""
        mlx_wrapper.initialisation()
        self.screen = mlx_wrapper.new_window(self.width, self.height)

    def create_image(self) -> None:
        """Put an image on the window, prepare the pixel to be written"""
        self.image = mlx_wrapper.new_image(self.width, self.height)
        self.pixels = mlx_wrapper.get_data_addr(self.image)

    def display_image(self):
        """Projecting the image onto the screen"""
        mlx_wrapper.destroy_image(self.image)
        self.pixels = None
        mlx_wrapper.blit_img(self.image, self.screen, (0, 0))
        mlx_wrapper.update_window()

    def fill_rectangle(
            self, x0: int, x1: int, y0: int, y1: int, color: str) -> None:
        x0, x1, y0, y1 = self.clip_rect(x0, x1, y0, y1)
        self.pixels[x0:x1, y0:y1] = color


class MazeDrawing():
    def __init__(self, engine: Renderer):
        """Maze color, cell_size, line_thickness"""
        self.edge_size = 40
        self.edge_color: int = 0x2121DE
        self.line_thickness = 10
        self.engine = engine

    def _get_thickness(self, middle: int) -> tuple[int, int]:
        """Calculate the offset for maze line thickness"""
        y0 = middle - (self.line_thickness // 2)
        y1 = middle + (self.line_thickness // 2)
        return (y0, y1)

    def _get_real_pos(self, index_x: int, index_y: int) -> tuple[int, int]:
        """Convert grid coordinates (column, row)
        to screen pixel coordinates."""
        pos_x = index_x * self.edge_size + self.engine.x_padding
        pos_y = index_y * self.edge_size + self.engine.y_padding
        return (pos_x, pos_y)

    def _draw_line(self, start: tuple[int, int]) -> None:
        """Draw an horizontal line from left to right"""
        x0, y_mid = start
        x1 = x0 + self.edge_size
        y0, y1 = self._get_thickness(y_mid)
        self.engine.fill_rectangle(x0, x1, y0, y1, self.edge_color)

    def _draw_column(self, start: tuple[int, int]) -> None:
        """Draw a vertical line from top to bottom"""
        x_middle, y0 = start
        y1 = y0 + self.edge_size
        x0, x1 = self._get_thickness(x_middle)
        self.engine.fill_rectangle(x0, x1, y0, y1, self.edge_color)

    def _draw_cell(self, cell_value: int, cell_pos: tuple[int, int]) -> None:
        """Draw walls for a single cell using bitwise masking.

        Bits convention:
            1 (0b0001): Top wall
            2 (0b0010): Right wall
            4 (0b0100): Bottom wall
            8 (0b1000): Left wall
        """
        x, y = cell_pos
        if cell_value & 1:
            self._draw_line((x, y))
        if cell_value & 2:
            self._draw_column((x + self.edge_size, y))
        if cell_value & 4:
            self._draw_line((x, y + self.edge_size))
        if cell_value & 8:
            self._draw_column((x, y))

    def draw_maze(self, maze: list[list[int]]):
        """Call the draw_cell function for each cell, effectively building
        the maze cell by cell"""
        for index_y, line in enumerate(maze):
            for index_x, cell in enumerate(line):
                cell_pos = self._get_real_pos(index_x, index_y)
                self._draw_cell(cell, cell_pos)


class PrototypeRendering():
    def __init__(self):
        pass

    def maze_generator(self, x, y):
        """Maze generator from A-MAZE-ING"""
        # Create a simple X x Y maze
        maze_gen = MazeGenerator((x, y))
        # Get the maze structure
        maze_grid = maze_gen.maze
        return maze_grid

    def dummy_windows_handler(self):
        """Prototype to keep the window running until an event happens"""
        running = True
        while running:
            events = mlx_wrapper.get_events()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

        mlx_wrapper.quit_window()

    def dummy_function_test(self, lab_width: int, lab_height: int):
        """Calls the Renderer and the MazeDrawing"""
        maze_file_python = self.maze_generator(lab_width, lab_height)
        engine = Renderer()
        engine.initialization()
        engine.create_image()
        maze = MazeDrawing(engine)
        maze.draw_maze(maze_file_python)
        engine.display_image()
        self.dummy_windows_handler()


pr = PrototypeRendering()
pr.dummy_function_test(int(sys.argv[1]), int(sys.argv[2]))
