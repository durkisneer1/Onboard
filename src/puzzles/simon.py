from typing import TYPE_CHECKING

import pygame as pg

if TYPE_CHECKING:
    from main import Engine


class SimonSaysPuzzle:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine
