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
        self.boop_sfx = pg.mixer.Sound("assets/boop.mp3")

    def update(self, active_list: list[Node]) -> None:
        left_click = pg.mouse.get_pressed()[0]
        mouse_pos = pg.mouse.get_pos()
        if left_click and abs((self.pos - mouse_pos).length()) < self.radius:
            self.active = True
            if self not in active_list:
                active_list.append(self)
                self.boop_sfx.play()

    def draw(self, screen: pg.Surface) -> None:
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

        self.tablet = pg.Surface((80, 80), pg.SRCALPHA)
        self.tablet_rect = self.tablet.get_rect(center=(WIN_WIDTH / 2, WIN_HEIGHT / 2))
        pg.draw.rect(
            self.tablet, (53, 54, 88), ((0, 0), self.tablet.size), border_radius=2
        )
        pg.draw.rect(
            self.tablet,
            (139, 151, 182),
            ((3, 3), self.tablet.size - pg.Vector2(6, 6)),
            border_radius=2,
        )
        pg.draw.rect(
            self.tablet,
            (40, 144, 220),
            ((4, 4), self.tablet.size - pg.Vector2(8, 8)),
            border_radius=2,
        )

        self.password = [0, 1, 2, 5]

        self.done = False
        self.success_sfx = pg.mixer.Sound("assets/success.mp3")

    def _draw_tablet(self) -> None:
        self.engine.screen.blit(self.tablet, self.tablet_rect)

    def _update_nodes(self) -> None:
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

        mouse_pos = pg.mouse.get_pos()
        # this is done so that the line toward mouse position
        # doesn't go outside the tablet's borders
        # (purely a visual change)
        clamped_mouse_pos = (
            max(92, min(WIN_WIDTH - 92, mouse_pos[0])),
            max(43, min(WIN_HEIGHT - 43, mouse_pos[1])),
        )
        if self.active_nodes:
            pg.draw.line(
                self.engine.screen,
                "white",
                self.active_nodes[-1].pos,
                clamped_mouse_pos,
            )

        if self.password == [node.num for node in self.active_nodes]:
            self.done = True
            self.active = False
            self.success_sfx.play()

    def _render(self) -> None:
        self._draw_tablet()
        self._update_nodes()
