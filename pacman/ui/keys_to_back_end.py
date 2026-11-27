from . import mlx_wrapper
import pygame
from ..entities import Direction
# from game import Game
from typing import Any


class ProcessKeys:
    def __init__(self):
        pass

    def handle_keys(self) -> Any:
        """For each key pressed, trigger a back_end event"""
        events = mlx_wrapper.get_events()
        for event in events:
            key = mlx_wrapper.get_key_pressed(event)
            if event.type == pygame.QUIT:
                return "QUIT"
            if key == "KEY_ESCAPE":
                return "QUIT"
            if key in ["KEY_W", "KEY_UP"]:
                return Direction.N
            if key in ["KEY_A", "KEY_LEFT"]:
                return Direction.W
            if key in ["KEY_S", "KEY_DOWN"]:
                return Direction.S
            if key in ["KEY_D", "KEY_RIGHT"]:
                return Direction.E
            if key == "KEY_C":
                return "TOGGLE_CHEAT"
            if key == "KEY_1":
                return "INVINCIBLE"
            if key == "KEY_2":
                return "FREEZE"
            if key == "KEY_3":
                return "ALWAYS_EDIBLE"
            if key == "KEY_4":
                return "SKIP_LEVEL"
            if key == "KEY_5":
                return "EXTRA_LIFE"

    def process_key(self) -> None:
        pass
