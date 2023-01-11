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
from src.constants import (
    COLOR_TRANSPARENT,
    TEXT_FONT,
    MUTE_SOUND,
    EFFECT_DURATION_MINI,
    EFFECT_DURATION_NORMAL,
    res_path,
)
from src.display.effect import (
    delayed_flag,
    alpha_effect,
    blur_effect,
    surface_blur,
)


class Button(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        text: str = "",
        on_press: Callable[
            [],
        ] = lambda: None,
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
                    self._abs_rect.collidepoint(event.pos)
                    and event.button == BUTTON_LEFT
                ):
                    if not MUTE_SOUND:
                        pygame.mixer.Sound(res_path("sound/sound2.ogg")).play()
                    on_press()

        self._handlers[MOUSEBUTTONDOWN].append(_mouse_button_down)

        self._on_mouse = False

        def _mouse_motion(event: pygame.event.Event):
            if self._visible:
                if self._abs_rect.collidepoint(event.pos):
                    if not self._on_mouse:
                        if not MUTE_SOUND:
                            pygame.mixer.Sound(
                                res_path("sound/sound1.ogg")
                            ).play()
                        self._on_mouse = True
                else:
                    self._on_mouse = False

        # self._handlers[MOUSEMOTION].append(_mouse_motion)

    def _shift_in(self):
        assert self._visible == False

        self._text.visible = True

        def onexit():
            self._visible = True
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

        self._flags["after_begin"].append(
            delayed_flag(
                self._flags["after_begin"],
                lambda: blur_effect(
                    self._surface,
                    "linear",
                    (0, self._blur),
                    EFFECT_DURATION_MINI,
                    onexit,
                ),
                EFFECT_DURATION_NORMAL - EFFECT_DURATION_MINI,
            )
        )

    def _shift_out(self):
        assert self._visible == True

        self._text.visible = False
        self._visible = False

        self._flags["after_begin"].append(
            blur_effect(
                self._surface, "linear", (self._blur, 0), EFFECT_DURATION_MINI
            )
        )

    def _draw_begin(self) -> None:
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

        def _shift_in(self):
            assert self._visible == False

            def onexit():
                self._visible = True

            self._flags["before_end"].append(
                alpha_effect(
                    self._text,
                    "ease_in",
                    (0, 255),
                    EFFECT_DURATION_NORMAL,
                    onexit,
                )
            )

        def _shift_out(self):
            assert self._visible == True

            def onexit():
                self._visible = False

            self._flags["before_end"].append(
                alpha_effect(
                    self._text,
                    "ease_out",
                    (255, 0),
                    EFFECT_DURATION_NORMAL,
                    onexit,
                )
            )

        def _draw_end(self) -> None:
            self._surface.blit(self._text, (0, 0))
