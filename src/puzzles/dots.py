from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg

from core.settings import WIN_HEIGHT, WIN_WIDTH
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class Node:
    def __init__(self, num: int, pos: pg.Vector2) -> None:
        self.num = num
        self.pos = pos
        self.radius = 5
        self.active = False

    def update(self, active_list: list[Node]):
        left_click = pg.mouse.get_pressed()[0]
        mouse_pos = pg.mouse.get_pos()
        if left_click and abs((self.pos - mouse_pos).length()) < self.radius:
            self.active = True
            if self not in active_list:
                active_list.append(self)

    def draw(self, screen):
        pg.draw.circle(screen, "white", self.pos, self.radius, 0 if self.active else 1)


class DotsPuzzle(Puzzle):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.nodes = [
            Node(
                x + y * 3,
                pg.Vector2(x, y) * 24 + (WIN_WIDTH / 2 - 24, WIN_HEIGHT / 2 - 24),
            )
            for x in range(0, 3)
            for y in range(0, 3)
        ]
        self.active_nodes = []

        self.password = [0, 1, 2, 5]

        self.done = False

    def _render(self):
        # pg.draw.rect(self.engine.screen, (1, 237,235), ())

        for node in self.nodes:
            node.update(self.active_nodes)
            node.draw(self.engine.screen)

        if pg.mouse.get_just_released()[0]:
            for node in self.active_nodes:
                node.active = False
            self.active_nodes.clear()

        if len(self.active_nodes) > 1:
            pg.draw.lines(
                self.engine.screen,
                "white",
                False,
                [node.pos for node in self.active_nodes],
            )

        if self.active_nodes:
            pg.draw.line(
                self.engine.screen,
                "white",
                self.active_nodes[-1].pos,
                pg.mouse.get_pos(),
            )

        if self.password == [node.num for node in self.active_nodes]:
            self.done = True
