from pacman.highscore import HighscoreEntry
from pydantic import ValidationError


class NameInput:
    def __init__(self, score: int) -> None:
        self.name = ""
        self.score = score

    def add_char(self, c: str) -> None:
        candidate = self.name + c
        try:
            HighscoreEntry(name=candidate, score=0)
        except ValidationError:
            return
        self.name = candidate

    def backspace(self) -> None:
        self.name = self.name[:-1]

    def submit(self) -> HighscoreEntry | None:
        try:
            name = HighscoreEntry(name=self.name, score=self.score)
        except ValidationError:
            return None
        return name
