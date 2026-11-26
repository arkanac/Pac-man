from typing import Any
from . import mlx_wrapper
from . import draw_sprites
from . import maze_draw
from . import keys_to_back_end as k
from pacman.game import Game, GameState
from pacman.entities import GhostState, Entity
from pacman.maze import Direction
import pygame


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
        self.engine: Renderer
        self.sp: draw_sprites.HandleSprite
        self.entities: pygame.Surface
        self.maze: maze_draw.MazeDrawing
        self.window: pygame.Surface
        self.maze_img: pygame.Surface
        self.game = game
        self.player = self.game.player
        self.edge = 100

    def _screen_pos(self, entity: Entity, t: float) -> tuple[int, int]:
        """Pixel position of an entity, sliding from its previous cell."""
        x = entity.prev_x + (entity.x - entity.prev_x) * t
        y = entity.prev_y + (entity.y - entity.prev_y) * t
        return (int(x * self.edge), int(y * self.edge))

    def draw_pacman(self, t: float) -> None:
        """Draw Pac-Man facing its direction, at its sliding position."""
        sprites = {
            Direction.N: "pacman_up",
            Direction.S: "pacman_down",
            Direction.E: "pacman_right",
            Direction.W: "pacman_left",
        }
        direction = self.game.player.current_direction
        name = sprites[direction] if direction else "pacman_right"
        self.sp.spawn_pacman(self.entities, name, 1,
                             self._screen_pos(self.game.player, t))

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

    def draw_entities(self, t: float) -> None:
        """Draw each ghost with its own sprite and state."""
        for ghost in self.game.ghosts:
            if ghost.state is GhostState.EATEN:
                continue
            if ghost.state is GhostState.EDIBLE:
                name = "blue"
            else:
                name = type(ghost).__name__.lower()
            self.sp.spawn_sprite(self.entities, name,
                                 self._screen_pos(ghost, t))

    def hud(self):
        self.sp.write_nbr(self.entities, (0, 0), str(self.game.score))

    def draw(self, t: float):
        """Draw one frame of the game"""
        mlx_wrapper.clear_window(self.maze_img)
        self.draw_pacgum()
        self.draw_super_pacgums()
        self.draw_entities(t)
        self.hud()
        self.draw_pacman(t)
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
