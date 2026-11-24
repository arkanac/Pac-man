from . import mlx_wrapper


class HandleSprite():
    def __init__(self, padding_x: int, padding_y: int):
        pacman_path = "pacman/ui/sprites/pacman.png"
        blinky_path = "pacman/ui/sprites/blinky.png"
        clyde_path = "pacman/ui/sprites/clyde.png"
        inky_path = "pacman/ui/sprites/inky.png"
        pinky_path = "pacman/ui/sprites/pinky.png"
        blueghost_path = "pacman/ui/sprites/blue_ghost.png"
        dot_path = "pacman/ui/sprites/dot.png"
        super_dot_path = "pacman/ui/sprites/strawberry.png"
        zero_p = "pacman/ui/sprites/numbers/Number0 7x10.png"
        one_p = "pacman/ui/sprites/numbers/Number1 7x10.png"
        two_p = "pacman/ui/sprites/numbers/Number2 7x10.png"
        three_p = "pacman/ui/sprites/numbers/Number3 7x10.png"
        four_p = "pacman/ui/sprites/numbers/Number4 7x10.png"
        five_p = "pacman/ui/sprites/numbers/Number5 7x10.png"
        six_p = "pacman/ui/sprites/numbers/Number6 7x10.png"
        seven_p = "pacman/ui/sprites/numbers/Number7 7x10.png"
        eight_p = "pacman/ui/sprites/numbers/Number8 7x10.png"
        nine_p = "pacman/ui/sprites/numbers/Number9 7x10.png"

        self.pacman = mlx_wrapper.load_sprite(pacman_path)
        self.blinky = mlx_wrapper.load_sprite(blinky_path)
        self.clyde = mlx_wrapper.load_sprite(clyde_path)
        self.inky = mlx_wrapper.load_sprite(inky_path)
        self.pinky = mlx_wrapper.load_sprite(pinky_path)
        self.blue_ghost = mlx_wrapper.load_sprite(blueghost_path)
        self.dot = mlx_wrapper.load_sprite(dot_path)
        self.super_dot = mlx_wrapper.load_sprite(super_dot_path)
        self.zero = mlx_wrapper.load_sprite(zero_p)
        self.one = mlx_wrapper.load_sprite(one_p)
        self.two = mlx_wrapper.load_sprite(two_p)
        self.three = mlx_wrapper.load_sprite(three_p)
        self.four = mlx_wrapper.load_sprite(four_p)
        self.five = mlx_wrapper.load_sprite(five_p)
        self.six = mlx_wrapper.load_sprite(six_p)
        self.seven = mlx_wrapper.load_sprite(seven_p)
        self.eight = mlx_wrapper.load_sprite(eight_p)
        self.nine = mlx_wrapper.load_sprite(nine_p)
        self.padding_y = padding_y
        self.padding_x = padding_x

    def spawn_sprite(self, surface, sprite_name: str, pos: tuple[int, int]):
        self.edge_size = 50
        self.line_thickness = 6
        x, y = pos
        y = (y + self.padding_y + self.edge_size / 2) - 5 + (self.line_thickness / 2) - 5
        x = (x + self.padding_x + self.edge_size / 2) - 5 + (self.line_thickness / 2) - 5
        match sprite_name:
            case "pacman":
                mlx_wrapper.blit_img(self.pacman, surface, (x - 5, y - 5))
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
            case "pacgum":
                mlx_wrapper.blit_img(self.dot, surface, (x, y))
            case "super_pacgum":
                mlx_wrapper.blit_img(self.super_dot, surface, (x, y))

    def write_nbr(self, surface, pos: tuple[int, int], number: str):
        for i, char in enumerate(number):
            x, y = pos
            x += i*7
            match char:
                case "0":
                    mlx_wrapper.blit_img(self.zero, surface, (x, y))
                case "1":
                    mlx_wrapper.blit_img(self.one, surface, (x, y))
                case "2":
                    mlx_wrapper.blit_img(self.two, surface, (x, y))
                case "3":
                    mlx_wrapper.blit_img(self.three, surface, (x, y))
                case "4":
                    mlx_wrapper.blit_img(self.four, surface, (x, y))
                case "5":
                    mlx_wrapper.blit_img(self.five, surface, (x, y))
                case "6":
                    mlx_wrapper.blit_img(self.six, surface, (x, y))
                case "7":
                    mlx_wrapper.blit_img(self.seven, surface, (x, y))
                case "8":
                    mlx_wrapper.blit_img(self.eight, surface, (x, y))
                case "9":
                    mlx_wrapper.blit_img(self.nine, surface, (x, y))
