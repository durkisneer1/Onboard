from typing import TYPE_CHECKING

import pygame as pg  # why

from core.settings import WIN_HEIGHT, WIN_WIDTH
from core.surfaces import import_image  # why

if TYPE_CHECKING:
    from main import Engine


class RangePicker:
    def __init__(
        self,
        engine: "Engine",
        pos: pg.Vector2,
        text: str,
        maxmin: list,
        default_per: int,
    ) -> None:
        self.engine = engine
        self.pos = pos
        self.text = text
        self.maxmin = maxmin
        self.default_per = default_per
        self.font = pg.font.Font("assets/m5x7.ttf", 16)

        self.text_surface = self.font.render(self.text, False, "white")
        self.overlay = self.font.render(
            f"{int((maxmin[1] - maxmin[0])*(self.default_per / 100) ):.0f}",
            False,
            [200, 200, 200],
        )

    def render(self) -> None:
        border_radius = 7

        rect = pg.Rect(0, 0, 0, 0)
        rect.width = 100
        rect.top = self.pos.y
        rect.height = self.text_surface.get_rect().height
        rect.right = (
            WIN_WIDTH - self.pos.x - 20
        )  # the 20 is for the controls width actually no f*ck the controls
        rect.inflate_ip(10, 2)

        hovering: bool = rect.collidepoint(pg.mouse.get_pos())
        holding: bool = pg.mouse.get_pressed()[0] and hovering

        masksurf = pg.Surface((rect.width, rect.height), pg.SRCALPHA).convert_alpha()
        pg.draw.rect(
            masksurf,
            (255, 255, 255),
            (0, 0, rect.width, rect.height),
            width=0,
            border_radius=border_radius,
        )
        mask = pg.mask.from_surface(masksurf)

        self.engine.screen.blit(self.text_surface, self.pos)
        rect_base = rect.copy()
        rect_base.width = rect.width * self.default_per / 100
        rect_base.left = rect.left

        masksurf.fill((0, 0, 0, 0))
        pg.draw.rect(
            masksurf, [30, 70, 70], (0, 0, rect_base.width, rect_base.height), 0, 0
        )
        mask.to_surface(masksurf, setcolor=None, unsetcolor=(0, 0, 0, 0))
        self.engine.screen.blit(masksurf, (rect_base.topleft))

        if hovering:
            pg.draw.rect(self.engine.screen, [30, 50, 50], rect, 1, border_radius)

        if holding:
            pg.draw.rect(self.engine.screen, [30, 100, 30], rect, 1, border_radius)
            mousepos = pg.mouse.get_pos()[0]
            mousepos -= rect.left - 1
            per = mousepos / rect.width
            self.default_per = per * 100
            self.overlay = self.font.render(
                f"{int((self.maxmin[1] - self.maxmin[0])*(self.default_per / 100) ):.0f}",
                False,
                [200, 200, 200],
            )
        if not holding and not hovering:
            pg.draw.rect(self.engine.screen, [30, 30, 30], rect, 1, border_radius)

        self.overlay_rect = self.overlay.get_rect()
        self.overlay_rect.center = rect.center
        self.engine.screen.blit(self.overlay, self.overlay_rect)
