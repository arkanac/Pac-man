from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated


class HighscoreEntry(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=10,
                                           strip_whitespace=True,
                                           pattern=r"^[A-Za-z0-9 ]+$")]
    score: Annotated[int, Field(ge=0)]
