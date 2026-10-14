MAIN = main.py

UI_DIR = pacman/ui
BACK_END_DIR = pacman

UI_FILES = end_screen.py \
           hud.py \
           menu.py \
           pause.py \
           renderer.py

BACK_END = app.py \
           cheats.py \
           config.py \
           entities.py \
           game.py \
           ghost_ai.py \
           highscore.py \
           level.py \
           maze.py

PY_FILES = $(MAIN) \
           $(addprefix $(UI_DIR)/,$(UI_FILES)) \
           $(addprefix $(BACK_END_DIR)/,$(BACK_END))

install:
	uv sync

run:
	uv run python $(MAIN) $(ARGS)

debug:
	uv run -m pdb $(MAIN) $(ARGS)

lint:
	uv run flake8 $(PY_FILES)
	uv run mypy $(PY_FILES) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

clean:
	@echo "Cleaning up Python files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +

.PHONY: install run debug clean lint