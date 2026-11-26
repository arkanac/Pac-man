from typing import Any
from . import mlx_wrapper
from . import draw_sprites
from . import maze_draw
from . import keys_to_back_end as k
from pacman.game import Game, GameState
from pacman.entities import GhostState
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
    def __init__(self, game: Game) -> None:
        self.width = 3000
        self.height = 1900
        self.engine = None
        self.sp = None
        self.entities = None
        self.maze = None
        self.window = None
        self.maze_img = None
        self.game = game
        self.player = self.game.player
        self.edge = 100


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

    def draw(self):
        """Draw one frame of the game"""
        mlx_wrapper.clear_window(self.maze_img)
        self.draw_pacgum()
        self.draw_super_pacgums()
        self.draw_entities()
        self.hud()
        self.draw_pacman()
        mlx_wrapper.blit_img(self.entities, self.maze_img, (0, 0))
        mlx_wrapper.clear_window(self.window)
        mlx_wrapper.clear_window(self.entities)
        self.maze.draw_maze(self.game.level.grid)
        self.engine.pixels = None
        mlx_wrapper.blit_img(self.maze_img, self.window, (0, 0))
        mlx_wrapper.update_window()

    def setup(self):
        """Create the window, images and sprites"""
        mlx_wrapper.initialisation()
        self.window = mlx_wrapper.new_window(self.width, self.height)
        self.maze_img = mlx_wrapper.new_image(self.width, self.height)
        self.maze_file = self.game.level.grid
        self.engine = Renderer(self.width, self. height)
        self.sp = draw_sprites.HandleSprite(
            self.engine.x_padding, self.engine.y_padding)
        self.maze = maze_draw.MazeDrawing(self.engine, self.maze_img)
        self.maze.draw_maze(self.game.level.grid)
        self.engine.pixels = None
        self.entities = mlx_wrapper.new_image(
            self.engine.width, self.engine.height)
