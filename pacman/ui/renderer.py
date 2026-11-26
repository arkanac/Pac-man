from typing import Any
from . import mlx_wrapper
from . import draw_sprites
from . import maze_draw
from . import keys_to_back_end as k
from pacman.game import Game, GameState
from pacman.entities import GhostState
from pacman.config import parse_config
from pacman.maze import Direction
import time


class Renderer():
    def __init__(self, width, height):
        """Useful variables for setting up the Visual Engine"""
        self.image = None
        self.pixels = None
        self.screen = None
        self.width = width
        self.height = height
        self.x_padding = 500
        self.y_padding = 200

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
    def __init__(self, config_path: str = "config.json") -> None:
        self.width = 3000
        self.height = 1900
        self.engine = None
        self.sp = None
        self.entities = None
        self.maze = None
        self.window = None
        self.maze_img = None
        self.maze_file = None
        self.config = parse_config(config_path)
        self.game = Game(self.config)
        self.turn = 0
        self.player = self.game.player
        self.edge = 100

    def game_running(self):
        """Prototype to keep the window running until an event happens"""
        running = True
        process_keys = k.ProcessKeys()
        while running:

            # process input
            action = process_keys.handle_keys()
            if action == "QUIT":
                running = False
            else:
                self.player.next_direction = action

            # print(f"Before: {self.player.x}, {self.player.y}")
            self.game.turn()
            if self.game.state is not GameState.PLAYING:
                running = False
            # print(f"After: {self.player.x}, {self.player.y}")

            # draw pacgums
            self.draw_pacgum()
            self.draw_super_pacgums()

            # draws entities
            self.draw_entities()

            # draw hud
            self.hud()

            # draw entities onto the maze img
            self.draw_pacman()
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
            time.sleep(1/5)

        # quit the window
        mlx_wrapper.quit_window()

    def draw_pacman(self):
        if self.game.player.current_direction is Direction.S:
            self.sp.spawn_pacman(self.entities, "pacman_down", 1, (self.player.x *self.edge, self.player.y*self.edge))
        if self.game.player.current_direction is Direction.N:
            self.sp.spawn_pacman(self.entities, "pacman_up", 1, (self.player.x *self.edge, self.player.y*self.edge))
        if self.game.player.current_direction is Direction.E:
            self.sp.spawn_pacman(self.entities, "pacman_right", 1, (self.player.x *self.edge, self.player.y*self.edge))
        if self.game.player.current_direction is Direction.W:
            self.sp.spawn_pacman(self.entities, "pacman_left", 1, (self.player.x *self.edge, self.player.y*self.edge))

    def draw_pacgum(self):
        pacgums = self.game.level.pacgums

        for pacgum in pacgums:
            x, y = pacgum
            self.sp.spawn_sprite(self.entities, "pacgum", (x*self.edge, y*self.edge))

    def draw_super_pacgums(self):
        super_pacgum = self.game.level.super_pacgums

        for sp in super_pacgum:
            x, y = sp
            self.sp.spawn_sprite(self.entities, "super_pacgum", (x*self.edge, y*self.edge))

    def draw_entities(self):
        if self.game.ghosts[0].state == GhostState.NORMAL:
            self.sp.spawn_sprite(self.entities, "pinky", (self.game.ghosts[0].x *self.edge, self.game.ghosts[0].y*self.edge))
            self.sp.spawn_sprite(self.entities, "inky", (self.game.ghosts[1].x*self.edge, self.game.ghosts[1].y*self.edge))
            self.sp.spawn_sprite(self.entities, "clyde", (self.game.ghosts[2].x *self.edge, self.game.ghosts[2].y*self.edge))
            self.sp.spawn_sprite(self.entities, "blinky", (self.game.ghosts[3].x*self.edge, self.game.ghosts[3].y*self.edge))
        if self.game.ghosts[0].state == GhostState.EDIBLE:
            self.sp.spawn_sprite(self.entities, "blue", (self.game.ghosts[0].x *self.edge, self.game.ghosts[0].y*self.edge))
            self.sp.spawn_sprite(self.entities, "blue", (self.game.ghosts[1].x*self.edge, self.game.ghosts[1].y*self.edge))
            self.sp.spawn_sprite(self.entities, "blue", (self.game.ghosts[2].x *self.edge, self.game.ghosts[2].y*self.edge))
            self.sp.spawn_sprite(self.entities, "blue", (self.game.ghosts[3].x*self.edge, self.game.ghosts[3].y*self.edge))

    def hud(self):
        self.sp.write_nbr(self.entities, (0, 0), str(self.game.score))

    def dummy_function_test(self):
        """Calls the Renderer and the MazeDrawing"""
        mlx_wrapper.initialisation()
        self.window = mlx_wrapper.new_window(self.width, self.height)
        self.maze_img = mlx_wrapper.new_image(self.width, self.height)
        self.maze_file = self.game.level.grid
        self.engine = Renderer(self.width, self. height)
        self.sp = draw_sprites.HandleSprite(
            self.engine.x_padding, self.engine.y_padding)
        self.maze = maze_draw.MazeDrawing(self.engine, self.maze_img)
        self.maze.draw_maze(self.maze_file)
        self.engine.pixels = None
        self.entities = mlx_wrapper.new_image(
            self.engine.width, self.engine.height)
        self.game_running()
