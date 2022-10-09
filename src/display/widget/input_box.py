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

File: src/display/widget/input_box.py
Description: General input box widget.
"""
import pygame
from pygame.constants import (
    MOUSEBUTTONDOWN,
    BUTTON_LEFT,
    K_RETURN,
    K_BACKSPACE,
    KEYDOWN,
)
from pygame.freetype import STYLE_UNDERLINE

from src.display.widget import Widget
from src.constants import COLOR_TRANSPARENT, COLOR_WHITE, TEXT_FONT, getpath
from src.display.effect import alpha_effect, blur_effect, surface_blur


class InputBox(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        default_text: str = "",
        text_hint: str = "",
    ) -> None:
        super().__init__(parent, rect, surface)
        self._blur = 50
        self._surface.set_alpha(0)
        self._visible = False

        self._activate_background = pygame.Surface(
            self._surface.get_size()
        ).convert_alpha()
        self._activate_background.fill(COLOR_WHITE)
        self._activate_background.set_alpha(0)
        self._activate = False

        self._foreground = pygame.Surface(
            self._surface.get_size()
        ).convert_alpha()
        self._foreground.fill(COLOR_TRANSPARENT)
        self._foreground.set_alpha(0)
        self.text = default_text
        self.text_hint = text_hint

        def _mouse_button_down(event: pygame.event.Event):
            if (
                self._visible
                and pygame.Rect(
                    *self._surface.get_abs_offset(), *self._surface.get_size()
                ).collidepoint(event.pos)
                and event.button == BUTTON_LEFT
            ):
                self.activate = True
            else:
                self.activate = False

        self._handlers[MOUSEBUTTONDOWN].append(_mouse_button_down)

    def _key_down(self, event: pygame.event.Event):
        if event.key == K_RETURN:
            # print(self.text)
            self.activate = False
        elif event.key == K_BACKSPACE:
            self.text = self.text[:-1]
        else:
            self.text += event.unicode

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
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

        self._flags.append(
            blur_effect(
                self._surface, "ease_in", (0, self._blur), duration, onexit
            )
        )
        self._flags.append(
            alpha_effect(self._foreground, "ease_in", (0, 255), duration)
        )
        self._flags.append(
            alpha_effect(
                self._activate_background, "ease_in", (0, 50), duration
            )
        )

    def shift_out(self, duration: float):
        assert self._visible == True

        self._visible = False

        self._flags.append(
            blur_effect(self._surface, "ease_out", (self._blur, 0), duration)
        )
        self._flags.append(
            alpha_effect(self._foreground, "ease_out", (255, 0), duration)
        )
        self._flags.append(
            alpha_effect(
                self._activate_background, "ease_out", (50, 0), duration
            )
        )

    @property
    def activate(self):
        return self._activate

    @activate.setter
    def activate(self, value: bool):
        if self._activate != value:
            if value:
                self.activate_in(0.2)
            else:
                self.activate_out(0.2)

    def activate_in(self, duration: float):
        assert self._activate == False

        def onexit():
            self._activate = True

        pygame.mixer.Sound(getpath("sound/sound1.ogg")).play()
        self._flags.append(
            alpha_effect(
                self._activate_background,
                "ease_in",
                (50, 150),
                duration,
                onexit,
            )
        )

        self._handlers[KEYDOWN].append(self._key_down)

    def activate_out(self, duration: float):
        assert self._activate == True

        def onexit():
            self._activate = False

        self._pre_flags.append(
            alpha_effect(
                self._activate_background,
                "ease_out",
                (150, 50),
                duration,
                onexit,
            )
        )

        self._handlers[KEYDOWN].remove(self._key_down)

    def draw_begin(self) -> None:
        if self._visible:
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

        self._foreground.fill(COLOR_TRANSPARENT)
        pygame.draw.rect(
            self._foreground, (0, 0, 0, 80), self._foreground.get_rect(), 2
        )

        text_surface = (
            TEXT_FONT.render(self.text)[0]
            if self.text != ""
            else TEXT_FONT.render(
                self.text_hint, (80, 80, 80), style=STYLE_UNDERLINE
            )[0]
        )
        if self._foreground.get_rect().contains(
            text_surface.get_rect(center=self._foreground.get_rect().center)
        ):
            self._foreground.blit(
                text_surface,
                text_surface.get_rect(
                    center=self._foreground.get_rect().center
                ),
            )
        else:
            self._foreground.blit(
                text_surface,
                text_surface.get_rect(
                    midright=self._foreground.get_rect().midright
                ),
            )

    def draw_end(self) -> None:
        self._surface.blit(self._activate_background, (0, 0))
        self._surface.blit(self._foreground, (0, 0))
