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

File: src/display/widget/button.py
Description: General button widget.
"""
from __future__ import annotations
import pygame
from pygame.constants import MOUSEBUTTONDOWN, BUTTON_LEFT, MOUSEMOTION
from typing import Callable

from src.display.widget import Widget
from src.constants import COLOR_TRANSPARENT, TEXT_FONT
from src.display.effect import alpha_effect, blur_effect, surface_blur


class Button(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        text: str = "",
        on_press: Callable[[],] = lambda: None,
    ) -> None:
        super().__init__(parent, rect, surface)
        self._blur = 50
        self._surface.set_alpha(0)
        self._visible = False
        self._text = Button.Text(self, rect, text)
        self._sub_widgets.append(self._text)

        def _mouse_button_down(event: pygame.event.Event):
            if self._visible:
                if (
                    pygame.Rect(
                        *self._surface.get_abs_offset(),
                        *self._surface.get_size()
                    ).collidepoint(event.pos)
                    and event.button == BUTTON_LEFT
                ):
                    pygame.mixer.Sound("res/sound/sound2.ogg").play()
                    on_press()

        self._handlers[MOUSEBUTTONDOWN].append(_mouse_button_down)

        self._on_mouse = False

        def _mouse_motion(event: pygame.event.Event):
            if self._visible:
                if pygame.Rect(
                    *self._surface.get_abs_offset(), *self._surface.get_size()
                ).collidepoint(event.pos):
                    if not self._on_mouse:
                        pygame.mixer.Sound("res/sound/sound1.ogg").play()
                        self._on_mouse = True
                else:
                    self._on_mouse = False

        # self._handlers[MOUSEMOTION].append(_mouse_motion)

    @Widget.visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self.shift_in(1)
                self._text.visible = True
            else:
                self.shift_out(1)
                self._text.visible = False

    def shift_in(self, duration: float):
        assert self._visible == False

        def onexit():
            self._visible = True
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

        self._pre_flags.append(
            blur_effect(
                self._surface, "ease_in", (0, self._blur), duration, onexit
            )
        )

    def shift_out(self, duration: float):
        assert self._visible == True

        self._visible = False

        self._pre_flags.append(
            blur_effect(self._surface, "ease_out", (self._blur, 0), duration)
        )

    def draw_begin(self) -> None:
        if self._visible == True:
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

    class Text(Widget):
        def __init__(
            self, parent: Widget, rect: pygame.Rect, text: str = ""
        ) -> None:
            surface = parent.surface
            super().__init__(parent, rect, surface)
            self._text = pygame.Surface(surface.get_size()).convert_alpha()
            self._text.fill(COLOR_TRANSPARENT)
            self._text_raw = TEXT_FONT.render(text)[0]
            self._text.blit(
                self._text_raw,
                self._text_raw.get_rect(center=self._text.get_rect().center),
            )
            pygame.draw.rect(
                self._text, (0, 0, 0, 80), self._text.get_rect(), 2
            )
            self._text.set_alpha(0)
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
                alpha_effect(self._text, "ease_in", (0, 255), duration, onexit)
            )

        def shift_out(self, duration: float):
            assert self._visible == True

            def onexit():
                self._visible = False

            self._flags.append(
                alpha_effect(self._text, "ease_out", (255, 0), duration, onexit)
            )

        def draw_end(self) -> None:
            self._surface.blit(self._text, (0, 0))
