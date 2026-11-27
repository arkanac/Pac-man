import time
from .config import parse_config
from .game import TURN_PER_SECOND, Game, GameState
from .maze import Direction
from .ui.renderer import PrototypeRendering
from .ui.keys_to_back_end import ProcessKeys
from .ui.mlx_wrapper import quit_window


def handle_cheat(game: Game, action: str) -> None:
    """Apply a cheat action; only TOGGLE_CHEAT works when cheats are off."""
    if action == "TOGGLE_CHEAT":
        game.cheats.toggle_cheat()
        return
    if not game.cheats.cheat_enabled:
        return
    if action == "INVINCIBLE":
        game.cheats.toggle_invincible()
    if action == "FREEZE":
        game.cheats.toggle_freeze()
    if action == "ALWAYS_EDIBLE":
        game.cheats.toggle_always_edible()
    if action == "SKIP_LEVEL":
        game.skip_level()
    if action == "EXTRA_LIFE":
        game.player.add_life()


def run(config_path: str) -> None:
    """Run  the game loop"""
    config = parse_config(config_path)
    game = Game(config)
    renderer = PrototypeRendering(game)
    renderer.setup()
    running = True
    process_keys = ProcessKeys()
    turn_duration = 1 / TURN_PER_SECOND
    frame_duration = 1 / 60
    accumulator = 0.0
    previous = time.perf_counter()
    while running:
        start = time.perf_counter()
        accumulator += start - previous
        previous = start
        action = process_keys.handle_keys()
        if action == "QUIT":
            running = False
        elif isinstance(action, Direction):
            game.player.set_direction(action)
        elif action is not None:
            handle_cheat(game, action)
        while accumulator >= turn_duration and running:
            accumulator -= turn_duration
            game.turn()
            if game.state is not GameState.PLAYING:
                running = False
        renderer.draw(accumulator / turn_duration)
        elapsed = time.perf_counter() - start
        if elapsed < frame_duration:
            time.sleep(frame_duration - elapsed)
    quit_window()
