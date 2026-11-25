import sys
from pacman.ui.renderer import PrototypeRendering


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 pac-man.py <config.json>")
    try:
        pr = PrototypeRendering(sys.argv[1])
        pr.dummy_function_test()
    except (FileNotFoundError, ValueError) as e:
        sys.exit(f"{e}")


if __name__ == "__main__":
    main()
