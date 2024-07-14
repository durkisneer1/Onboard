import json
from typing import TYPE_CHECKING

import pygame as pg

from core.buttons import SimonButton
from core.settings import SCN_SIZE
from core.surfaces import import_image

if TYPE_CHECKING:
    from main import Engine


class Diary:
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine

        self.progress = 1

        self.clip_width = SCN_SIZE[0] // 2
        self.clip_height = SCN_SIZE[1] * 2 / 3

        # Tablet Background
        self.tablet = pg.Surface(
            (self.clip_width + 3, self.clip_height + 8), pg.SRCALPHA
        )
        self.tablet_rect = self.tablet.get_rect(midleft=(3, SCN_SIZE[1] / 2))
        pg.draw.rect(
            self.tablet, (53, 54, 88), ((0, 0), self.tablet.size), border_radius=2
        )
        pg.draw.rect(
            self.tablet,
            (139, 151, 182),
            ((2, 2), self.tablet.size - pg.Vector2(4, 4)),
            border_radius=2,
        )

        # Bloom
        self.tablet_bloom = pg.Surface(
            self.tablet.size + pg.Vector2(20, 20), pg.SRCALPHA
        )
        pg.draw.rect(
            self.tablet_bloom,
            "white",
            ((5, 5), self.tablet.size + pg.Vector2(10, 10)),
            border_radius=2,
        )
        self.tablet_bloom = pg.transform.gaussian_blur(self.tablet_bloom, 6)
        self.tablet_bloom.set_alpha(60)

        with open("assets/logs.json", "r") as f:
            logs_dict = json.loads(f.read())

        self.keys = ["none", "cockpit", "storage", "reactor"]
        self.key_idx = 0
        self.logs = {
            key: engine.px_font.render(
                logs_dict[key], False, (24, 13, 47), wraplength=self.clip_width
            )
            for key in self.keys
        }

        self.current_log = self.logs[self.keys[self.key_idx]]

        self.y_offset = 0
        self.view = self.current_log.subsurface(
            (0, self.y_offset, self.clip_width, self.clip_height)
        )
        self.view_rect = self.view.get_frect(midleft=(8, SCN_SIZE[1] / 2))

        btn_surfs = {
            "idle": import_image("assets/arrow_normal.png"),
            "hover": import_image("assets/arrow_hover.png"),
            "pressed": import_image("assets/arrow_press.png"),
        }
        self.buttons = [
            SimonButton(engine, 0, pg.Vector2(self.view_rect.bottomleft), btn_surfs),
            SimonButton(engine, 1, pg.Vector2(self.view_rect.midbottom), btn_surfs),
        ]

        self.closed = True
        self.instruction = engine.px_font.render("SPACE to toggle", False, (24, 13, 47))
        self.instruction_rect = self.instruction.get_rect(
            bottomright=(SCN_SIZE[0] - 3, SCN_SIZE[1])
        )

    def handle_events(self, event: pg.Event):
        if event.type == pg.MOUSEWHEEL:
            self.y_offset -= event.precise_y * 4
            self.y_offset = pg.math.clamp(
                self.y_offset, 0, self.current_log.height - self.clip_height
            )
            self.view = self.current_log.subsurface(
                (0, self.y_offset, self.clip_width, self.clip_height)
            )
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.closed = not self.closed
            elif event.key == pg.K_LEFT:
                self.key_idx -= 1
                self.update()
            elif event.key == pg.K_RIGHT:
                self.key_idx += 1
                self.update()

    def update(self):
        self.key_idx %= self.progress
        self.current_log = self.logs[self.keys[self.key_idx]]
        self.view = self.current_log.subsurface(
            (0, self.y_offset, self.clip_width, self.clip_height)
        )

    def render(self):
        if self.closed:
            return

        # Tablet
        self.engine.screen.blit(self.tablet, self.tablet_rect)

        # Bloom
        self.engine.screen.blit(self.tablet_bloom, self.tablet_rect.move(-10, -10))

        # Screen
        pg.draw.rect(
            self.engine.screen,
            "white",
            (
                self.tablet_rect.topleft + pg.Vector2(4, 4),
                self.tablet.size - pg.Vector2(8, 8),
            ),
            border_radius=2,
        )

        # Text
        self.engine.screen.blit(self.view, self.view_rect)
        self.engine.screen.blit(self.instruction, self.instruction_rect)
