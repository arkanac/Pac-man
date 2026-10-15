from pydantic import BaseModel, Field
from typing import Annotated
import commentjson


class Rules(BaseModel):
    lives: Annotated[int, Field(gt=0)]
    pacgum: Annotated[int, Field(gt=0)]
    point_per_pacgum: Annotated[int, Field(gt=0)]
    point_per_super_pacgum: Annotated[int, Field(gt=0)]
    point_per_ghost: Annotated[int, Field(gt=0)]


class LevelSpecs(BaseModel):
    level: Annotated[int, Field(gt=0, le=10)]
    width: Annotated[int, Field(gt=0)]
    height: Annotated[int, Field(gt=0)]
    level_max_time: Annotated[int, Field(gt=0)]


class GameConfig(BaseModel):
    model_config = {"frozen": True}

    seed: int | str
    highscore_filename: str
    rules: Rules
    game_specs: list[LevelSpecs]


def parse_config(filename: str = "config.json") -> GameConfig:
    """Verify the config file and load it with Pydantic."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = commentjson.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not open file: {e}") from e
    except Exception as e:
        raise ValueError(f"Invalid JSON syntax in {filename}: {e}") from e
    try:
        config = GameConfig.model_validate(data)
    except ValueError as e:
        raise ValueError(f"Incorrect value in Config file: {e}") from e
    return config
