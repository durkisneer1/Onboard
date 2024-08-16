import json
from typing import TYPE_CHECKING

import pygame as pg

from core.settings import SCN_SIZE
from core.surfaces import import_image

if TYPE_CHECKING:
    from main import Engine


class Diary:
    TOLERANCE = 0.1
    LERP_SPEED = 10
    
    def __init__(self, engine: "Engine") -> None:
        self.engine = engine

        self.progress = 1

        self.clip_width = SCN_SIZE[0] // 2
        self.clip_height = SCN_SIZE[1] * 2 / 3

        # Tablet Background
        self.tablet = pg.Surface(
            (self.clip_width + 3, self.clip_height + 8), pg.SRCALPHA
        )
        self.tablet_rect = self.tablet.get_frect(midleft=(-self.tablet.width, SCN_SIZE[1] / 2))
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

        self.closed_x = -self.tablet.width
        self.open_x = 3
        self.opening = False
        self.on = False
        self.hidden = True

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
                self.opening = not self.opening
                if self.opening:
                    self.hidden = False
                else:
                    self.on = False
            elif event.key == pg.K_LEFT:
                self.engine.diary.y_offset = 0
                self.key_idx -= 1
                self.update()
            elif event.key == pg.K_RIGHT:
                self.engine.diary.y_offset = 0
                self.key_idx += 1
                self.update()

    def update(self):
        self.key_idx %= self.progress
        self.current_log = self.logs[self.keys[self.key_idx]]
        self.view = self.current_log.subsurface(
            (0, self.y_offset, self.clip_width, self.clip_height)
        )

    def render(self):
        if self.hidden:
            return
        
        target_x = self.open_x if self.opening else self.closed_x
        if abs(self.tablet_rect.x - target_x) > self.TOLERANCE:
            self.tablet_rect.x = pg.math.lerp(self.tablet_rect.x, target_x, self.engine.dt * self.LERP_SPEED)
        else:
            if self.opening:
                self.on = True
            else:
                self.hidden = True

        # Tablet
        self.engine.screen.blit(self.tablet, self.tablet_rect)

        if not self.on:
            # Screen Off
            pg.draw.rect(
                self.engine.screen,
                "black",
                (
                    self.tablet_rect.topleft + pg.Vector2(4, 4),
                    self.tablet.size - pg.Vector2(8, 8),
                ),
                border_radius=2,
            )
            return

        # Bloom
        self.engine.screen.blit(self.tablet_bloom, self.tablet_rect.move(-10, -10))

        # Screen On
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
