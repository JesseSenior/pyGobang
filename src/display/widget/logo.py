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

File: src/display/widget/LOGO.py
Description: LOGO
"""
from __future__ import annotations
import pygame
from random import choice
from typing import Tuple
from src.constants import getpath

from src.display.widget import Widget
from src.display.effect import alpha_effect


class LOGO(Widget):
    def __init__(
        self, parent: Widget, pos: Tuple[int, int], scale: float
    ) -> None:
        self._logo_img = pygame.image.load(
            choice(
                [
                    getpath("image/LOGO_dark.png"),
                    getpath("image/LOGO_light.png"),
                ]
            )
        ).convert_alpha()
        parent_surface_size = parent.surface.get_size()
        rect = pygame.Rect(*pos, 0, 0).inflate(
            parent_surface_size[0] * scale, parent_surface_size[1] * scale
        )
        rect = self._logo_img.get_rect().fit(rect)

        super().__init__(parent, rect)
        self._logo_img = pygame.transform.smoothscale(self._logo_img, rect.size)
        self._logo_img.set_alpha(0)
        self._visible = False

    @Widget.visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self.shift_in(1)
            else:
                self.shift_out(1)

    def shift_in(self, duration: float):
        assert self._visible == False

        def onexit():
            self._visible = True

        self._flags.append(
            alpha_effect(self._logo_img, "ease_in", (0, 255), duration, onexit)
        )

    def shift_out(self, duration: float):
        assert self._visible == True

        def onexit():
            self._visible = False

        self._flags.append(
            alpha_effect(self._logo_img, "ease_out", (255, 0), duration, onexit)
        )

    def draw_end(self) -> None:
        self._surface.blit(self._logo_img, (0, 0))
