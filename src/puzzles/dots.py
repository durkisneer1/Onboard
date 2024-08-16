from __future__ import annotations

from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE
from core.surfaces import import_image
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class Node:
    def __init__(self, engine: "Engine", num: int, pos: pg.Vector2) -> None:
        self.num = num
        self.pos = pos
        self.radius = 5
        self.active = False
        self.boop_sfx = engine.sfx["boop"]

    def update(self, active_list: list[Node], mouse_pos: pg.Vector2):
        left_click = pg.mouse.get_pressed()[0]
        if left_click and abs((self.pos - mouse_pos).length()) < self.radius:
            self.active = True
            if self not in active_list:
                active_list.append(self)
                self.boop_sfx.play()

    def draw(self, screen: pg.Surface):
        pg.draw.circle(screen, "white", self.pos, 2, 0)
        if self.active:
            pg.draw.circle(screen, "white", self.pos, self.radius, 1)


class DotsPuzzle(Puzzle):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)

        self.nodes = [
            Node(
                engine,
                x + y * 3,
                pg.Vector2(x, y) * 24 + (SCN_SIZE[0] / 2 - 24, SCN_SIZE[1] / 2 - 24),
            )
            for x in range(0, 3)
            for y in range(0, 3)
        ]
        self.active_nodes = []

        # Tablet Background
        self.tablet = pg.Surface((80, 80), pg.SRCALPHA)
        self.tablet_rect = self.tablet.get_rect(
            center=(SCN_SIZE[0] / 2, SCN_SIZE[1] / 2)
        )
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

        self.password = [6, 3, 0, 4, 2, 1, 5, 7, 8]

        self.done = False

        self.checkmark_img = import_image("assets/check.png")
        self.checkmark_rect = self.checkmark_img.get_rect(
            center=pg.Vector2(SCN_SIZE) / 2
        )
        self.checkmark_timer = 2000  # 2s
        self.done_time = 0
        self.start_timer = False

        self.hint = engine.px_font.render("find the password", False, (24, 13, 47))
        self.hint_pos = self.hint.get_rect(bottomleft=(4, SCN_SIZE[1]))

    def _draw_tablet(self):
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

    def _update_nodes(self):
        if not self.start_timer:
            for node in self.nodes:
                node.update(self.active_nodes, self.engine.mouse_pos)
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

        # this is done so that the line toward mouse position
        # doesn't go outside the tablet's borders
        # (purely a visual change)
        clamped_mouse_pos = (
            max(92, min(SCN_SIZE[0] - 92, self.engine.mouse_pos.x)),
            max(43, min(SCN_SIZE[1] - 43, self.engine.mouse_pos.y)),
        )
        if self.active_nodes:
            pg.draw.line(
                self.engine.screen,
                "white",
                self.active_nodes[-1].pos,
                clamped_mouse_pos,
            )

        # so that it doesn't matter which node you start from
        user_in = [node.num for node in self.active_nodes]
        if self.password == user_in or self.password[::-1] == user_in:
            self.active_nodes.clear()
            if not self.start_timer:
                self.engine.sfx["success"].play()
                self.done_time = pg.time.get_ticks()
                self.start_timer = True

        if self.start_timer:
            if pg.time.get_ticks() - self.done_time > self.checkmark_timer:
                self.done = True
                self.active = False

    def _render(self):
        self._draw_tablet()
        self._update_nodes()
        self.engine.screen.blit(self.hint, self.hint_pos)
