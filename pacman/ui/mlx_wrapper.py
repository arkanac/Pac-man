import pygame
import numpy as np
from typing import Any
# from ..errors import ViewError
from pathlib import Path


def initialisation() -> None:
    """Initialize import modules"""
    pygame.init()


def new_window(width: int, height: int) -> pygame.Surface:
    """Create and initialize a graphical window(width, height)"""
    return pygame.display.set_mode((width, height))


def quit_window() -> None:
    """Closing pygame window"""
    pygame.quit()


def new_image(width: int, height: int) -> pygame.Surface:
    """Create an image on top of the window or other
    images size(width, height)"""
    return pygame.Surface((width, height))


def update_window() -> None:
    """Tells X11 we need to update the current physical screen
    with the current img buffer"""
    pygame.display.update()


def load_sprite(path: Path) -> pygame.Surface:
    """Translating the png sprite into a pygame image"""
    try:
        return pygame.image.load(path).convert_alpha()
    except FileNotFoundError as e:
        raise ViewError(e)
    except PermissionError as e:
        raise ViewError(e)


def blit_img(image: pygame.Surface,
             dest_screen: pygame.Surface,
             coords: tuple[int, int]) -> None:
    """Project the choosen img onthe the screen"""
    dest_screen.blit(image, coords)


def to_buffer(sprite: pygame.Surface,
              set_black_transparency: bool = True) -> np.ndarray:
    """Draw the sprite onto the image buffer"""
    pixels = pygame.surfarray.pixels2d(sprite)

    if set_black_transparency:
        masks = sprite.get_masks()

        rgb_mask = masks[0] | masks[1] | masks[2]

        pixels[(pixels & rgb_mask) == 0] = 0

    return pixels.T.ravel()


def get_data_addr(image: pygame.Surface) -> np.ndarray:
    """Create a new 2D array that directly
    references the pixel values in a Surface"""
    return pygame.surfarray.pixels2d(image)


def destroy_image(image: pygame.Surface) -> None:
    """The img need to be unlocked to blit """
    image.unlock()


def get_events() -> list[pygame.event.Event] | Any:
    """Getting events from event queue"""
    return pygame.event.get()


def get_padding() -> int:
    """Return a fixed padding value"""
    return 500


def _get_key_mapping() -> dict[int, str]:
    """Convert the key_mapping values from pygames names to mlx names"""
    return {
        pygame.K_w: "KEY_W",
        pygame.K_s: "KEY_S",
        pygame.K_a: "KEY_A",
        pygame.K_d: "KEY_D",
        pygame.K_p: "KEY_P",
        pygame.K_c: "KEY_C",
        pygame.K_1: "KEY_1",
        pygame.K_2: "KEY_2",
        pygame.K_3: "KEY_3",
        pygame.K_4: "KEY_4",
        pygame.K_5: "KEY_5",
        pygame.K_6: "KEY_6",
        pygame.K_BACKSPACE: "KEY_BACKSPACE",
        pygame.K_RETURN: "KEY_RETURN",
        pygame.K_SPACE: "KEY_SPACE"
    }


def get_key_pressed(event: pygame.event.Event) -> str | None:
    """Convert the event into the actual key pressed"""
    if event.type == pygame.KEYDOWN:
        mapping = _get_key_mapping()
        mapped_key = mapping.get(event.key, None)
        if mapped_key:
            return mapped_key
        is_letter = pygame.K_a <= event.key <= pygame.K_z
        is_number = pygame.K_0 <= event.key <= pygame.K_9
        is_space = event.key == pygame.K_SPACE
        if is_letter or is_number or is_space:
            char = chr(event.key)
            return f"CHAR_{char}"
    return None


def clear_window(window: pygame.Surface) -> None:
    """Clear the buffer with zeros (memset)"""
    window.fill((0, 0, 0))
