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

File: src/display/widget/background.py
Description: The widget for general background.
"""

from __future__ import annotations
import pygame
import threading
from typing import Tuple

from src.display.widget import Widget
from src.constants import (
    COLOR_BACKGROUND,
    COLOR_BLACK,
    COLOR_TRANSPARENT,
    WINDOW_SIZE,
    EFFECT_DURATION_MINI,
    EFFECT_DURATION_NORMAL,
    EFFECT_DURATION_HUGE,
    res_path,
)
from src.display.effect import blur_effect, alpha_effect, surface_blur
from src.display.texture import generate_texture


class Background(Widget):
    def __init__(
        self,
        size: Tuple[int, int] = WINDOW_SIZE,
        img_path=res_path("image/background.png"),
        default_color=COLOR_BACKGROUND,
        enable_shader=True,
    ) -> None:
        super().__init__(None, None, False)
        self._img_path = img_path
        self._default_color = default_color
        self._enable_shader = enable_shader
        self._thread = threading.Thread(
            target=self.generate_background, args=[size]
        )
        self._thread.start()
        if self._enable_shader:
            self._shader = pygame.Surface(size).convert_alpha()
            self._shader.fill(COLOR_TRANSPARENT)
            pygame.draw.rect(
                self._shader,
                COLOR_BLACK,
                self._shader.get_rect(),
                min(WINDOW_SIZE) // 50,
            )
            self._shader = surface_blur(self._shader, min(WINDOW_SIZE) // 10)
            self._shader.set_alpha(50)

            def breath_in():
                self._flags["before_end"].append(
                    alpha_effect(
                        self._shader,
                        "ease_in_out",
                        (50, 150),
                        EFFECT_DURATION_HUGE,
                        breath_out,
                    )
                )

            def breath_out():
                self._flags["before_end"].append(
                    alpha_effect(
                        self._shader,
                        "ease_in_out",
                        (150, 50),
                        EFFECT_DURATION_HUGE,
                        breath_in,
                    )
                )

            breath_in()

    @property
    def background_prepared(self):
        return hasattr(self, "_background")

    def set_surface(
        self, parent: Widget, rect: pygame.Rect, surface: pygame.Surface = None
    ):
        if self._parent != parent:
            self._parent = parent
            self._surface = (
                parent.surface.subsurface(rect) if surface == None else surface
            )

    def generate_background(self, size: Tuple[int, int]):
        try:
            self._background_img = generate_texture(self._img_path, size)
            self._background = pygame.Surface(self._background_img.get_size())

            self._flags["before_end"].append(
                blur_effect(
                    self._background_img,
                    "ease_in",
                    (50, 1),
                    EFFECT_DURATION_NORMAL + EFFECT_DURATION_MINI,
                    target_surface=self._background,
                )
            )
            self._flags["before_end"].append(
                alpha_effect(
                    self._background,
                    "ease_in",
                    (0, 255),
                    EFFECT_DURATION_NORMAL,
                )
            )
        except:
            pass

    def _draw_begin(self) -> None:
        self._surface.fill(self._default_color)

    def _draw_end(self) -> None:
        if hasattr(self, "_background"):
            self._surface.blit(self._background, (0, 0))
        if self._enable_shader:
            self._surface.blit(self._shader, (0, 0))
