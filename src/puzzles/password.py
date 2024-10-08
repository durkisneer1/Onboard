from random import choice
from typing import TYPE_CHECKING
import json

import pygame as pg

from core.settings import SCN_SIZE
from src.puzzles.puzzle import Puzzle

if TYPE_CHECKING:
    from main import Engine


class PasswordPuzzle(Puzzle):
    NAMES = [
        "Amelia",
        "Evelyn",
        "Olivia",
        "Charlotte",
        "Isabella",
        "Calista",
        "Luna",
        "Aurora",
        "Scarlett",
        "Maeve",
    ]

    def __init__(self, engine: "Engine") -> None:
        super().__init__(engine)
        self.done = False

        self.sfx = [
            pg.mixer.Sound(f"assets/keypresses/key{i}.mp3") for i in range(1, 5)
        ]

        # Tablet
        self.tablet = pg.Surface((100, 20), pg.SRCALPHA)
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
        self.tablet_bloom = pg.Surface((120, 40), pg.SRCALPHA)
        pg.draw.rect(
            self.tablet_bloom,
            "white",
            ((8, 19), self.tablet.size - pg.Vector2(36, 38)),
            border_radius=2,
        )
        self.tablet_bloom = pg.transform.gaussian_blur(self.tablet_bloom, 8)
        self.tablet_bloom.set_alpha(10)

        self.chosen_name = choice(self.NAMES)
        self.code = self.chosen_name.lower()
        self.user_in = ""

        # Change name in json
        with open("assets/logs.json", "r") as f:
            data = json.loads(f.read())
        data["reactor"] = data["reactor"].replace("$name$", self.chosen_name)
        with open("assets/logs.json", "w") as f:
            json.dump(data, f, indent=2)
        
        self.text_coord = self.tablet_rect.midleft + pg.Vector2(6, -1)
        self._generate_text(True)

        self.hint = engine.px_font.render("who do you love?", False, (24, 13, 47))
        self.hint_pos = self.hint.get_rect(bottomleft=(4, SCN_SIZE[1]))

    def _reset_json_name(self):
        with open("assets/logs.json", "r") as f:
            data = json.loads(f.read())
        data["reactor"] = data["reactor"].replace(self.chosen_name, "$name$")
        with open("assets/logs.json", "w") as f:
            json.dump(data, f, indent=2)

    def handle_events(self, event):
        if event.type == pg.TEXTINPUT and len(self.user_in) < 14:
            self.user_in += event.text
            self._generate_text()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                self.user_in = self.user_in[:-1]
                self._generate_text()
            elif event.key == pg.K_RETURN:
                choice(self.sfx).play()
                if self.user_in.lower() == self.code:
                    self.active = False
                    self.done = True
                    self.engine.sfx["success"].play()
                    self._reset_json_name()
                else:
                    self.engine.sfx["failure"].play()

    def _generate_text(self, first: bool = False):
        self.text_surf = self.engine.px_font.render(self.user_in, False, "white")
        self.text_rect = self.text_surf.get_rect(midleft=self.text_coord)
        if not first:
            choice(self.sfx).play()

    def _render(self):
        # Screen
        self.engine.screen.blit(self.tablet, self.tablet_rect)
        pg.draw.rect(
            self.engine.screen,
            "black",
            (
                self.tablet_rect.topleft + pg.Vector2(4, 4),
                self.tablet.size - pg.Vector2(8, 8),
            ),
            border_radius=2,
        )
        self.engine.screen.blit(self.tablet_bloom, self.tablet_rect.move(10, 0))

        self.engine.screen.blit(self.text_surf, self.text_rect)
        self.engine.screen.blit(self.hint, self.hint_pos)
