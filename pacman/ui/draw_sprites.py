import mlx_wrapper


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

    def draw_pacgums():
        pass
