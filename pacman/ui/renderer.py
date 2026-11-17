from typing import Any
from mazegenerator import MazeGenerator
from . import mlx_wrapper
from . import draw_sprites
from . import maze_draw
from . import keys_to_back_end as k
from pacman.game import Game
from pacman.config import parse_config
import time


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
        self.game = Game(parse_config("config.json"))
        self.turn = 0
        self.player = self.game.player

    def maze_generator(self, x, y):
        """Maze generator from A-MAZE-ING"""
        # Create a simple X x Y maze
        maze_gen = MazeGenerator((x, y))
        # Get the maze structure
        maze_grid = maze_gen.maze
        return maze_grid

    def game_running(self):
        """Prototype to keep the window running until an event happens"""
        running = True
        x0 = 10
        y0 = 10
        process_keys = k.ProcessKeys()
        while running:

            # process input
            action = process_keys.handle_keys()
            if action == "QUIT":
                running = False
            else:
                pass

            # UPDATE (Game folder)
            print(f"Before: {self.player.x}, {self.player.y}")
            self.game.turn()
            print(f"After: {self.player.x}, {self.player.y}")

            # draws entities
            self.sp.spawn_sprite(self.entities, "pacman", (self.player.x, self.player.y))
            self.sp.spawn_sprite(self.entities, "pinky", (40, y0))
            self.sp.spawn_sprite(self.entities, "inky", (70, y0))

            # draw entities onto the maze img
            mlx_wrapper.blit_img(self.entities, self.maze_img, (0, 0))

            # refresh both the entities window and the main window
            mlx_wrapper.clear_window(self.window)
            mlx_wrapper.clear_window(self.entities)

            # draw the maze onto the window
            self.maze.draw_maze(self.maze_file)
            self.engine.pixels = None

            # blit the maze onto the window
            mlx_wrapper.blit_img(self.maze_img, self.window, (0, 0))

            # push the modifications to the surface
            mlx_wrapper.update_window()

            # sleep for 1/60 seconds (for 60 fps)
            time.sleep(1)

        # quit the window
        mlx_wrapper.quit_window()

    def dummy_function_test(self, lab_width: int, lab_height: int):
        """Calls the Renderer and the MazeDrawing"""
        mlx_wrapper.initialisation()
        self.window = mlx_wrapper.new_window(self.width, self.height)
        self.maze_img = mlx_wrapper.new_image(self.width, self.height)
        self.maze_file = self.maze_generator(lab_width, lab_height)
        self.engine = Renderer(self.width, self. height)
        self.sp = draw_sprites.HandleSprite(
            self.engine.x_padding, self.engine.y_padding)
        self.maze = maze_draw.MazeDrawing(self.engine, self.maze_img)
        self.maze.draw_maze(self.maze_file)
        self.engine.pixels = None
        self.entities = mlx_wrapper.new_image(
            self.engine.width, self.engine.height)
        self.game_running()


pr = PrototypeRendering()
pr.dummy_function_test(15, 15)
