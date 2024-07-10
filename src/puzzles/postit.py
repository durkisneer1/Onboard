from typing import TYPE_CHECKING

from core.settings import *
from core.surfaces import import_image
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class PostItPuzzle(Puzzle):
    def __init__(self, engine: "Engine"):
        super().__init__(engine)

        self.image = import_image("assets/post_it.png")

    def _render(self) -> None:
        self.engine.screen.blit(self.image, (WIN_WIDTH / 2 - 32, WIN_HEIGHT / 2 - 32))
