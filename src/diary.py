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

        self.progress = 1  # Default 1

        self.clip_width = SCN_SIZE[0] // 2
        self.clip_height = SCN_SIZE[1] * 2 / 3

        # Tablet Background
        self.tablet = pg.Surface(
            (self.clip_width + 4, self.clip_height + 10), pg.SRCALPHA
        )
        self.tablet_rect = self.tablet.get_frect(
            midleft=(-self.tablet.width, SCN_SIZE[1] / 2)
        )
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

        # Button to open and close diary
        self.toggle_btn = import_image("assets/diary_toggle.png")
        self.toggle_btn_rect = self.toggle_btn.get_frect(
            midleft=(self.tablet_rect.right + 4, SCN_SIZE[1] / 2)
        )

        # Buttons to flip pages
        self.left_btn = import_image("assets/tablet_flip.png")
        self.right_btn = pg.transform.flip(self.left_btn, True, False)
        self.right_btn_rect = self.right_btn.get_frect(
            bottomright=(
                self.tablet.width - 3,
                self.tablet_rect.bottom - 5,
            )  # 126 is from
        )
        self.left_btn_rect = self.left_btn.get_frect(
            topright=self.right_btn_rect.topleft
        ).move(-3, 0)

        # Page index dots
        self.dots_surface = pg.Surface((7, 1), pg.SRCALPHA)
        self.dots_surface_rect = self.dots_surface.get_rect(
            midtop=(self.tablet.width // 2 + 3, self.tablet_rect.top + 5)
        )
        self.dot_positions = [(x, 0) for x in range(0, 7, 2)]
        for pos in self.dot_positions:
            pg.draw.rect(self.dots_surface, (104, 107, 114), (pos, (1, 1)))
        self.gray_dots = self.dots_surface.copy()
        self.update()

    def handle_events(self, event: pg.Event):
        if event.type == pg.MOUSEWHEEL:
            self.y_offset -= event.precise_y * 4
            self.y_offset = pg.math.clamp(
                self.y_offset, 0, self.current_log.height - self.clip_height
            )
            self.view = self.current_log.subsurface(
                (0, self.y_offset, self.clip_width, self.clip_height)
            )
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
            if self.toggle_btn_rect.collidepoint(self.engine.mouse_pos):
                self.opening = not self.opening
                if self.opening:
                    self.hidden = False
                else:
                    self.on = False
                self.toggle_btn = pg.transform.flip(self.toggle_btn, True, False)
            elif self.left_btn_rect.collidepoint(self.engine.mouse_pos):
                self.engine.diary.y_offset = 0
                self.key_idx -= 1
                self.update()
            elif self.right_btn_rect.collidepoint(self.engine.mouse_pos):
                self.engine.diary.y_offset = 0
                self.key_idx += 1
                self.update()

    def update(self):
        self.key_idx %= self.progress
        self.current_log = self.logs[self.keys[self.key_idx]]
        self.view = self.current_log.subsurface(
            (0, self.y_offset, self.clip_width, self.clip_height)
        )
        self.dots_surface.blit(self.gray_dots)
        pg.draw.rect(
            self.dots_surface, "black", (self.dot_positions[self.key_idx], (1, 1))
        )

    def render(self):
        self.engine.screen.blit(self.toggle_btn, self.toggle_btn_rect)

        if self.hidden:
            return

        target_x = self.open_x if self.opening else self.closed_x
        if abs(self.tablet_rect.x - target_x) > self.TOLERANCE:
            self.tablet_rect.x = pg.math.lerp(
                self.tablet_rect.x, target_x, self.engine.dt * self.LERP_SPEED
            )
            self.toggle_btn_rect.x = self.tablet_rect.right + 4
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

        # Page turn buttons
        self.engine.screen.blit(self.left_btn, self.left_btn_rect)
        self.engine.screen.blit(self.right_btn, self.right_btn_rect)

        # Page index dots
        self.engine.screen.blit(self.dots_surface, self.dots_surface_rect)
