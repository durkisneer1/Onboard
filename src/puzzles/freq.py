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

        self.tablet_surf = pg.Surface((100, 100))
        self.tablet_surf.fill("white")
        self.tablet_rect = self.tablet_surf.get_rect(
            center=(SCN_SIZE[0] // 2, SCN_SIZE[1] // 2)
        )

        self.template_wave = TemplateWave()
        self.matching_wave = MatchWave()

        self.actions = {
            pg.K_UP: lambda: self.matching_wave.edit_amp(inc=True),
            pg.K_DOWN: lambda: self.matching_wave.edit_amp(dec=True),
            pg.K_LEFT: lambda: self.matching_wave.edit_stretch(dec=True),
            pg.K_RIGHT: lambda: self.matching_wave.edit_stretch(inc=True),
        }

        self.success_sfx = pg.mixer.Sound("assets/success.mp3")

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
                self.success_sfx.play()

    def _render(self):
        self.update()

        self.engine.screen.blit(self.tablet_surf, self.tablet_rect)
        self.template_wave.draw(self.engine.screen, "blue")
        self.matching_wave.draw(self.engine.screen, "red")
        self.engine.screen.blit(self.hint, self.hint_pos)
