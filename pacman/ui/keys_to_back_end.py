import mlx_wrapper
import pygame
# from game import Game


class ProcessKeys:
    def __init__(self):
        pass

    def handle_keys(self) -> str:
        """For each key pressed, trigger a back_end event"""
        events = mlx_wrapper.get_events()
        for event in events:
            key = mlx_wrapper.get_key_pressed(event)
            if event.type == pygame.QUIT:
                return "QUIT"
            if key == "KEY_W":
                return "UP"
            if key == "KEY_A":
                return "LEFT"
            if key == "KEY_S":
                return "DOWN"
            if key == "KEY_D":
                return "RIGHT"

    def process_key(self) -> None:
        pass
