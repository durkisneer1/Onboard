import inspect
import os
from typing import TYPE_CHECKING

import pygame as pg

from core.settings import *

if TYPE_CHECKING:
    from main import Engine


image_load = pg.image.load
pg_surface = pg.Surface

surface_debug = True


def import_folder(
    path: str,
    is_alpha: bool = True,
    scale: float = 1,
    highlight: bool = False,
    blur: bool = False,
) -> list[pg.Surface]:
    surf_list = []
    for _, __, img_file in os.walk(path):
        for image in img_file:
            if not image.endswith(".png"):
                continue

            full_path = path + "/" + image
            surface = import_image(full_path, is_alpha, scale, highlight, blur)
            surf_list.append(surface)
    return surf_list


def import_image(
    path: str,
    is_alpha: bool = True,
    scale: float = 1,
    highlight: bool = False,
    blur: bool = False,
) -> pg.Surface:
    image_surf = (
        pg.image.load(path).convert_alpha()
        if is_alpha
        else pg.image.load(path).convert()
    )

    if scale != 1 and scale > 0:
        image_surf = pg.transform.scale_by(image_surf, scale)
    if highlight:
        image_surf.fill((40, 40, 40, 0), special_flags=pg.BLEND_RGB_ADD)
    if blur:
        template_surf = pg.Surface(
            (image_surf.width + 20, image_surf.height + 20), pg.SRCALPHA
        )
        template_surf.fill((0, 0, 0, 0))
        image_rect = image_surf.get_frect(
            center=(template_surf.width / 2, template_surf.height / 2)
        )
        template_surf.blit(image_surf, image_rect)
        image_surf = pg.transform.gaussian_blur(template_surf, 5)

    return image_surf


def import_anim(path: str, width: int, height: int) -> list[pg.Surface]:
    anim_surf = import_image(path)
    anim_list = [
        anim_surf.subsurface((x, 0, width, height))
        for x in range(0, anim_surf.width, width)
    ]
    return anim_list


def shift_colors(
    surface: pg.Surface, color_sets: list[list[tuple[int, int, int]]], n: int
) -> pg.Surface:
    surface = surface.copy()
    array = pg.PixelArray(surface)
    for colors in color_sets:
        for old_color, new_color in zip(colors, [(0, 0, 0)] * n + colors):
            array.replace(old_color, new_color)

    return surface


def new_image_load(*args, **kwargs):
    current_frame = inspect.currentframe()
    if current_frame is None or current_frame.f_back is None:
        return

    calling_file = current_frame.f_back.f_globals["__file__"]
    calling_file = os.path.basename(calling_file)
    if surface_debug:
        print(f"IMAGE_LOAD: '{args[0]}' in '{calling_file}'")
    return image_load(*args, **kwargs)


def new_surface(*args, **kwargs):
    current_frame = inspect.currentframe()
    if current_frame is None or current_frame.f_back is None:
        return

    calling_file = current_frame.f_back.f_globals["__file__"]
    calling_file = os.path.basename(calling_file)
    if surface_debug:
        print(f"NEW_SURFACE: '{calling_file}'")
    return pg_surface(*args, **kwargs)


pg.image.load = new_image_load
pg.Surface = new_surface
