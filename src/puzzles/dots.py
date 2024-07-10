from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from core.surfaces import import_image
from core.settings import WIN_HEIGHT, WIN_SIZE, WIN_WIDTH
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
        pg.draw.circle(screen, "white", self.pos, 2, 0)
        if self.active:
            pg.draw.circle(screen, "white", self.pos, self.radius, 1)


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

        # Tablet Background
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

        # Bloom
        self.tablet_bloom = pg.Surface((100, 100), pg.SRCALPHA)
        pg.draw.rect(
            self.tablet_bloom,
            (40, 144, 220),
            ((5, 5), self.tablet.size + pg.Vector2(10, 10)),
            border_radius=2,
        )
        self.tablet_bloom = pg.transform.gaussian_blur(self.tablet_bloom, 6)
        self.tablet_bloom.set_alpha(100)

        self.password = [0, 1, 2, 5]

        self.done = False
        self.success_sfx = pg.mixer.Sound("assets/success.mp3")

        self.checkmark_img = import_image("assets/check.png")
        self.checkmark_rect = self.checkmark_img.get_rect(center=pg.Vector2(WIN_SIZE) / 2)
        self.checkmark_timer = 2000  # 2s
        self.done_time = 0
        self.start_timer = False

    def _draw_tablet(self) -> None:
        self.engine.screen.blit(self.tablet, self.tablet_rect)
        self.engine.screen.blit(self.tablet_bloom, self.tablet_rect.move(-10, -10))

        # Screen
        pg.draw.rect(
            self.engine.screen,
            (94, 233, 233),
            (
                self.tablet_rect.topleft + pg.Vector2(4, 4),
                self.tablet.size - pg.Vector2(8, 8),
            ),
            border_radius=2,
        )

    def _update_nodes(self) -> None:
        if not self.start_timer:
            for node in self.nodes:
                node.update(self.active_nodes)
                node.draw(self.engine.screen)

            if pg.mouse.get_just_released()[0]:
                for node in self.active_nodes:
                    node.active = False
                self.active_nodes.clear()
        else:
            self.engine.screen.blit(self.checkmark_img, self.checkmark_rect)

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
            self.active_nodes.clear()
            if not self.start_timer:
                self.success_sfx.play()
                self.done_time = pg.time.get_ticks()
                self.start_timer = True

        if self.start_timer:
            if pg.time.get_ticks() - self.done_time > self.checkmark_timer:
                self.done = True
                self.active = False

    def _render(self) -> None:
        self._draw_tablet()
        self._update_nodes()
