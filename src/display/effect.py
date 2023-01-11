"""pyGobang, a python based Gobang game.

Copyright (C) 2022 Jesse Senior

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program.  If not, see <http://www.gnu.org/licenses/>.

File: src/display/effect.py
Description: The implementation for effect in GUI.
"""
import pygame
from math import floor
from typing import Callable, Tuple
from PIL import Image, ImageFilter

from src.display.tool import image_to_surface, surface_to_image
from src.constants import COLOR_TRANSPARENT

transformers = {
    "linear": lambda x: x,
    "ease_in": lambda x: x * x,
    "ease_out": lambda x: 2 * x - x * x,
    "ease_in_out": lambda x: 2 * x * x
    if x <= 0.5
    else 1 - (2 - 2 * x) ** 2 / 2,
}


def transform(begin: Tuple, end: Tuple, duration: float, type: str):
    assert len(begin) == len(end)
    transformer = transformers[type]
    timer = pygame.time.Clock()
    total_tick = floor(duration * 1000)
    current_tick = timer.tick()
    while current_tick < total_tick:
        yield tuple(
            floor(
                begin[i]
                + (end[i] - begin[i]) * transformer(current_tick / total_tick)
            )
            for i in range(len(begin))
        )
        current_tick += timer.tick()
    yield tuple(
        floor(begin[i] + (end[i] - begin[i]) * transformer(1))
        for i in range(len(begin))
    )


def surface_blur(surface: pygame.Surface, blur: int):
    return image_to_surface(
        surface_to_image(surface).filter(ImageFilter.BoxBlur(blur))
    )


def surface_mosaic(surface: pygame.Surface, granularity: int):
    width, height = surface.get_size()
    return image_to_surface(
        surface_to_image(surface)
        .resize(
            (width // granularity, height // granularity),
            resample=Image.BILINEAR,
        )
        .resize((width, height), Image.NEAREST)
    )


class Flag:
    def __init__(self, parent, on_exit=None) -> None:
        self._parent = parent
        self._on_exit = on_exit
        self._is_finished = False
        pass

    @property
    def is_finished(self) -> bool:
        return self._is_finished

    def exit(self):
        if self._on_exit != None:
            self._on_exit()
        self._is_finished = True

    def execute(self) -> None:
        pass


class SurfaceFlag(Flag):
    def __init__(
        self,
        surface: pygame.Surface,
        target_surface: pygame.Surface = None,
        on_exit=None,
    ) -> None:
        super().__init__(None, on_exit)
        self._surface = surface
        self._target_surface = (
            target_surface if target_surface != None else surface
        )


class delayed_flag(Flag):
    def __init__(
        self, flag_list: list, waiting_flag: Callable[[], Flag], time: float
    ) -> None:
        super().__init__(None)
        self._waiting_flag = waiting_flag
        self._flag_list = flag_list
        self._timer = pygame.time.Clock()
        self._tick = floor(time * 1000)  # Convert to millisecond

    def execute(self) -> None:
        if self._tick > 0:
            self._tick -= self._timer.tick()
        else:
            self._flag_list.append(self._waiting_flag())
            self.exit()


class temporary_flag(Flag):
    def __init__(self, parent, on_exit=None) -> None:
        super().__init__(parent, on_exit)

    def execute(self) -> None:
        self.exit()


class blur_effect(SurfaceFlag):
    def __init__(
        self,
        surface: pygame.Surface,
        transform_type: str,
        blur: Tuple[int, int],
        duration: float,
        on_exit=None,
        target_surface=None,
    ) -> None:
        super().__init__(surface, target_surface, on_exit)
        self._transformer_blur = transform(
            (blur[0],), (blur[1],), duration, transform_type
        )

    def execute(self) -> None:
        try:
            tmp = surface_blur(self._surface, next(self._transformer_blur)[0])
            self._target_surface.fill(COLOR_TRANSPARENT)
            self._target_surface.blit(tmp, (0, 0))
        except StopIteration:
            self.exit()


class mosaic_effect(SurfaceFlag):
    def __init__(
        self,
        surface: pygame.Surface,
        transform_type: str,
        granularity: Tuple[int, int],
        duration: float,
        on_exit=None,
        target_surface=None,
    ) -> None:
        super().__init__(surface, target_surface, on_exit)
        self._transformer_granularity = transform(
            (granularity[0],), (granularity[1],), duration, transform_type
        )

    def execute(self) -> None:
        try:
            tmp = surface_mosaic(
                self._surface, next(self._transformer_granularity)[0]
            )
            self._target_surface.fill(COLOR_TRANSPARENT)
            self._target_surface.blit(tmp, (0, 0))
        except StopIteration:
            self.exit()


class alpha_effect(SurfaceFlag):
    def __init__(
        self,
        surface: pygame.Surface,
        transform_type: str,
        alpha: Tuple[int, int],
        duration: float,
        on_exit=None,
    ) -> None:
        super().__init__(surface, None, on_exit)
        self._transformer_alpha = transform(
            (alpha[0],), (alpha[1],), duration, transform_type
        )

    def execute(self) -> None:
        try:
            self._target_surface.set_alpha(next(self._transformer_alpha)[0])
        except StopIteration:
            self.exit()
