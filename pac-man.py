import sys
from pacman.app import run


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 pac-man.py <config.json>")
    try:
        run(sys.argv[1])
    except (FileNotFoundError, ValueError) as e:
        sys.exit(f"{e}")


if __name__ == "__main__":
    main()
