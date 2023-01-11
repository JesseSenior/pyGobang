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

File: src/display/widget/text.py
Description: General text widget.
"""
from __future__ import annotations
import pygame

from src.display.widget import Widget
from src.constants import COLOR_TRANSPARENT, TEXT_FONT, EFFECT_DURATION_NORMAL
from src.display.effect import alpha_effect


class Text(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        text: str = "",
    ) -> None:
        super().__init__(parent, rect, surface)
        self._visible = False
        self._text = text
        self._surface_raw = pygame.Surface(
            self._surface.get_size()
        ).convert_alpha()

        self._text_raw = TEXT_FONT.render(self._text)[0]

        self._surface_raw.set_alpha(0)
        self._visible = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        if self._text != value:
            self._text = value
            self._text_raw = TEXT_FONT.render(self._text)[0]

    def _shift_in(self):
        assert self._visible == False

        self._visible = True

        self._flags["before_end"].append(
            alpha_effect(
                self._surface_raw, "linear", (0, 255), EFFECT_DURATION_NORMAL
            )
        )

    def _shift_out(self):
        assert self._visible == True

        self._visible = False

        self._flags["before_end"].append(
            alpha_effect(
                self._surface_raw, "linear", (255, 0), EFFECT_DURATION_NORMAL
            )
        )

    def _draw_begin(self) -> None:
        self._surface_raw.fill(COLOR_TRANSPARENT)
        self._surface_raw.blit(
            self._text_raw,
            self._text_raw.get_rect(
                midleft=self._surface_raw.get_rect().midleft
            ),
        )

    def _draw_end(self) -> None:
        self._surface.blit(self._surface_raw, (0, 0))
