import random
from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE
from core.surfaces import import_image
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class PostItPuzzle(Puzzle):
    def __init__(self, engine: "Engine"):
        super().__init__(engine)

        self.image = import_image("assets/post_it.png")

    def _render(self) -> None:
        self.engine.screen.blit(
            self.image, (SCN_SIZE[0] / 2 - 32, SCN_SIZE[1] / 2 - 32)
        )


class PoemPuzzle(Puzzle):
    def __init__(self, engine: "Engine"):
        super().__init__(engine)

        self.image = import_image(f"assets/poem{str(random.randint(1, 2))}.png")
        self.rect = self.image.get_frect(center=(SCN_SIZE[0] / 2, SCN_SIZE[1] / 2))

    def _render(self) -> None:
        self.engine.screen.blit(self.image, self.rect)
