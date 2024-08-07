from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE
from core.surfaces import import_image
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class Wire:
    def __init__(
        self,
        surface_uncut: pg.Surface,
        surface_cut: pg.Surface,
        pos: pg.Vector2,
        color: tuple[int, int, int],
    ):
        self.surface_uncut = surface_uncut
        self.surface_cut = surface_cut
        self.rect = self.surface_cut.get_rect(topleft=pos)

        self.surface_uncut.fill(color, special_flags=pg.BLEND_MULT)
        self.surface_cut.fill(color, special_flags=pg.BLEND_MULT)

        self.cut = False
        self.event = False
        self.hovered = False

    def render(self, screen: pg.Surface, mouse_pos: pg.Vector2):
        surf = self.surface_cut if self.cut else self.surface_uncut
        screen.blit(surf, self.rect)

        self.event = False
        self.hovered = False
        if self.rect.collidepoint(mouse_pos) and not self.cut:
            self.hovered = True
            # pg.draw.rect(screen, "yellow", self.rect, 1)
            if pg.mouse.get_just_pressed()[0]:
                self.cut = True
                self.event = True


class WireCut(Puzzle):
    def __init__(self, engine: "Engine"):
        super().__init__(engine)
        self.engine = engine

        self.background = import_image("assets/wire_box.png")
        self.scissors = import_image("assets/scissors.png")
        wires_uncut = import_image("assets/uncut.png")
        wires_cut = import_image("assets/cut.png")

        self.rect = wires_cut.get_frect(center=(SCN_SIZE[0] / 2, SCN_SIZE[1] / 2))
        self.background_rect = self.rect.inflate(6, 6)
        # subsurface each wire from global image
        wire_colors = [
            (255, 70, 70),
            (70, 255, 70),
            (70, 70, 255),
            (255, 200, 70),
            (70, 255, 255),
        ]
        wire_rects = [pg.Rect(pg.Vector2(5 + 16 * i, 0), (6, 64)) for i in range(5)]
        self.wires = []
        for i, rect in enumerate(wire_rects):
            wire = Wire(
                wires_uncut.subsurface(rect),
                wires_cut.subsurface(rect),
                self.rect.topleft + pg.Vector2(rect.topleft) + pg.Vector2(0, 1),
                wire_colors[i],
            )
            self.wires.append(wire)

        # in what order to cut the wires
        self.combination = [2, 0, 3]
        self.user_in = []

        self.hint = engine.px_font.render("cut in the order", False, (24, 13, 47))
        self.hint_pos = self.hint.get_rect(bottomright=(SCN_SIZE[0] - 4, SCN_SIZE[1]))

        self.done = False

    def reset(self):
        for wire in self.wires:
            wire.cut = False
        self.user_in = []

    def _render(self):
        self.engine.screen.blit(self.background, self.background_rect)

        for wire in self.wires:
            wire.render(self.engine.screen, self.engine.mouse_pos)

            if wire.hovered:
                self.engine.screen.blit(
                    self.scissors, self.engine.mouse_pos - pg.Vector2(6, 6)
                )

            if wire.event:
                self.engine.sfx["cut"].play()
                self.user_in.append(self.wires.index(wire))

        if self.combination == self.user_in:
            self.active = False
            self.done = True
            self.engine.sfx["success"].play()
            self.engine.diary.y_offset = 0
            self.engine.diary.progress += 1
            self.engine.diary.key_idx += 1
            self.engine.diary.update()

        self.engine.screen.blit(self.hint, self.hint_pos)
