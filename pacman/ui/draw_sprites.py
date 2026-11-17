from . import mlx_wrapper


class HandleSprite():
    def __init__(self, padding_x: int, padding_y: int):
        pacman_path = "pacman/ui/sprites/pacman.png"
        blinky_path = "pacman/ui/sprites/blinky.png"
        clyde_path = "pacman/ui/sprites/clyde.png"
        inky_path = "pacman/ui/sprites/inky.png"
        pinky_path = "pacman/ui/sprites/pinky.png"
        blueghost_path = "pacman/ui/sprites/blue_ghost.png"
        self.pacman = mlx_wrapper.load_sprite(pacman_path)
        self.blinky = mlx_wrapper.load_sprite(blinky_path)
        self.clyde = mlx_wrapper.load_sprite(clyde_path)
        self.inky = mlx_wrapper.load_sprite(inky_path)
        self.pinky = mlx_wrapper.load_sprite(pinky_path)
        self.blue_ghost = mlx_wrapper.load_sprite(blueghost_path)
        self.padding_y = padding_y
        self.padding_x = padding_x

    def spawn_sprite(self, surface, sprite_name: str, pos: tuple[int, int]):
        x, y = pos
        y = y + self.padding_y
        x = x + self.padding_x
        match sprite_name:
            case "pacman":
                mlx_wrapper.blit_img(self.pacman, surface, (x, y))
            case "blinky":
                mlx_wrapper.blit_img(self.blinky, surface, (x, y))
            case "clyde":
                mlx_wrapper.blit_img(self.clyde, surface, (x, y))
            case "inky":
                mlx_wrapper.blit_img(self.inky, surface, (x, y))
            case "pinky":
                mlx_wrapper.blit_img(self.pinky, surface, (x, y))
            case "blue":
                mlx_wrapper.blit_img(self.blue_ghost, surface, (x, y))

    def draw_pacgums():
        pass
