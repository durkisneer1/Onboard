from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE
from src.puzzles.puzzle import Puzzle
from src.puzzles.waves import MatchWave, TemplateWave

if TYPE_CHECKING:
    from main import Engine


class FreqPuzzle(Puzzle):
    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)
        self.done = False
        self.amount_completed = 0

        # Tablet
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
            "white",
            ((8, 8), self.tablet.size - pg.Vector2(36, 36)),
            border_radius=2,
        )
        self.tablet_bloom = pg.transform.gaussian_blur(self.tablet_bloom, 8)
        self.tablet_bloom.set_alpha(10)

        self.template_wave = TemplateWave()
        self.matching_wave = MatchWave()

        self.actions = {
            pg.K_UP: lambda: self.matching_wave.edit_amp(inc=True),
            pg.K_DOWN: lambda: self.matching_wave.edit_amp(dec=True),
            pg.K_LEFT: lambda: self.matching_wave.edit_stretch(dec=True),
            pg.K_RIGHT: lambda: self.matching_wave.edit_stretch(inc=True),
        }

        font = pg.Font("assets/m5x7.ttf", 16)
        self.hint = font.render("match the sound", False, (24, 13, 47))
        self.hint_pos = self.hint.get_rect(bottomleft=(4, SCN_SIZE[1]))

    def update(self) -> None:
        just_pressed = pg.key.get_just_pressed()

        for key, action in self.actions.items():
            if just_pressed[key]:
                action()
                break

        if just_pressed[pg.K_RETURN]:
            if self.template_wave != self.matching_wave:
                return

            self.template_wave.reset()
            self.amount_completed += 1
            if self.amount_completed == 6:
                self.done = True
                self.active = False
                self.engine.sfx["success"].play()

    def _render(self):
        self.update()

        self.engine.screen.blit(self.tablet, self.tablet_rect)
        # Screen
        pg.draw.rect(
            self.engine.screen,
            "black",
            (
                self.tablet_rect.topleft + pg.Vector2(4, 4),
                self.tablet.size - pg.Vector2(8, 8),
            ),
            border_radius=2,
        )
        self.engine.screen.blit(self.tablet_bloom, self.tablet_rect.move(10, 10))

        self.template_wave.draw(self.engine.screen)
        self.matching_wave.draw(self.engine.screen)
        self.engine.screen.blit(self.hint, self.hint_pos)
