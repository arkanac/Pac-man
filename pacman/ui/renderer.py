import mlx_wrapper
from typing import Any
# from ..maze import Enum
import pygame
from mazegenerator import MazeGenerator


class Renderer():
    def __init__(self, width, height):
        """Useful variables for setting up the Visual Engine"""
        self.image = None
        self.pixels: Any = None
        self.screen = None
        self.width = width
        self.height = height
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

    def fill_rectangle(
            self, x0: int, x1: int, y0: int, y1: int, color: str, img) -> None:
        x0, x1, y0, y1 = self.clip_rect(x0, x1, y0, y1)
        self.pixels = mlx_wrapper.get_data_addr(img)
        self.pixels[x0:x1, y0:y1] = color


class MazeDrawing():
    def __init__(self, engine: Renderer, maze_img):
        """Maze color, cell_size, line_thickness"""
        self.edge_size = 50
        self.edge_color: int = 0x2121DE
        self.line_thickness = 6
        self.engine = engine
        self.maze_img = maze_img

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
        self.engine.fill_rectangle(x0, x1, y0, y1,
                                   self.edge_color, self.maze_img)

    def _draw_column(self, start: tuple[int, int]) -> None:
        """Draw a vertical line from top to bottom"""
        x_middle, y0 = start
        y1 = y0 + self.edge_size
        x0, x1 = self._get_thickness(x_middle)
        self.engine.fill_rectangle(x0, x1, y0, y1, self.edge_color,
                                   self.maze_img)

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


class HandleSprite():
    def __init__(self):
        pacman_path = "pacman/ui/sprites/pacman.png"
        blinky_path = "pacman/ui/sprites/blinky.png"
        clyde_path = "pacman/ui/sprites/clyde.png"
        inky_path = "pacman/ui/sprites/inky.png"
        pinky_path = "pacman/ui/sprites/pinky.png"
        self.pacman = mlx_wrapper.load_sprite(pacman_path)
        self.blinky = mlx_wrapper.load_sprite(blinky_path)
        self.clyde = mlx_wrapper.load_sprite(clyde_path)
        self.inky = mlx_wrapper.load_sprite(inky_path)
        self.pinky = mlx_wrapper.load_sprite(pinky_path)

    def spawn_sprite(surface, sprite, pos: tuple[int, int]):
        mlx_wrapper.blit_img(sprite, surface, pos)


class PrototypeRendering():
    def __init__(self):
        self.width = 1500
        self.height = 1200
        self.engine = None
        self.sp = None
        self.entities = None
        self.maze = None
        self.window = None
        self.maze_img = None
        self.maze_file = None

    def maze_generator(self, x, y):
        """Maze generator from A-MAZE-ING"""
        # Create a simple X x Y maze
        maze_gen = MazeGenerator((x, y))
        # Get the maze structure
        maze_grid = maze_gen.maze
        return maze_grid

    def handle_keys(self) -> bool:
        """For each key pressed, trigger a back_end event"""
        events = mlx_wrapper.get_events()
        for event in events:
            key = mlx_wrapper.get_key_pressed(event)
            if event.type == pygame.QUIT:
                return False
            if key == "KEY_W":
                return True
            if key == "KEY_A":
                return True
            if key == "KEY_S":
                return True
            if key == "KEY_D":
                return True
        return True

    def game_running(self):
        """Prototype to keep the window running until an event happens"""
        running = True
        x0 = 10
        y0 = 10
        pacman = self.sp.pacman
        while running:
            running = self.handle_keys()
            mlx_wrapper.blit_img(pacman, self.entities, (
                x0 + self.engine.x_padding, y0 + self.engine.y_padding))
            mlx_wrapper.blit_img(self.entities, self.maze_img, (0, 0))
            mlx_wrapper.clear_window(self.window)
            mlx_wrapper.clear_window(self.entities)
            self.maze.draw_maze(self.maze_file)
            self.engine.pixels = None
            mlx_wrapper.blit_img(self.maze_img, self.window, (0, 0))
            mlx_wrapper.update_window()

        mlx_wrapper.quit_window()

    def dummy_function_test(self, lab_width: int, lab_height: int):
        """Calls the Renderer and the MazeDrawing"""
        mlx_wrapper.initialisation()
        self.window = mlx_wrapper.new_window(self.width, self.height)
        self.maze_img = mlx_wrapper.new_image(self.width, self.height)
        self.maze_file = self.maze_generator(lab_width, lab_height)
        self.engine = Renderer(self.width, self. height)
        self.sp = HandleSprite()
        self.maze = MazeDrawing(self.engine, self.maze_img)
        self.maze.draw_maze(self.maze_file)
        self.engine.pixels = None
        self.entities = mlx_wrapper.new_image(
            self.engine.width, self.engine.height)
        self.game_running()


pr = PrototypeRendering()
pr.dummy_function_test(15, 15)
