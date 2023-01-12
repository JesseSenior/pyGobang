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
    K_KP_ENTER,
    K_BACKSPACE,
    KEYDOWN,
    TEXTINPUT,
    TEXTEDITING,
)
from pygame.freetype import STYLE_UNDERLINE

from src.display.widget import Widget
from src.display.tool import play_sound
from src.constants import (
    COLOR_TRANSPARENT,
    COLOR_WHITE,
    EFFECT_DURATION_TINY,
    EFFECT_DURATION_MINI,
    EFFECT_DURATION_NORMAL,
    TEXT_FONT,
)
from src.display.effect import (
    delayed_flag,
    alpha_effect,
    blur_effect,
    surface_blur,
)


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
        self._visible = False
        self._visible_full = False
        self._activate = False

        self._background = pygame.Surface(
            self._surface.get_size()
        ).convert_alpha()
        self._background.fill(COLOR_WHITE)
        self._background.set_alpha(0)

        self._foreground = pygame.Surface(
            self._surface.get_size()
        ).convert_alpha()
        self._foreground.fill(COLOR_TRANSPARENT)
        self._foreground.set_alpha(0)
        self.text = default_text
        self._editing_text = ""
        self.text_hint = text_hint

        def _mouse_button_down(event: pygame.event.Event):
            if (
                self._visible
                and self._abs_rect.collidepoint(event.pos)
                and event.button == BUTTON_LEFT
            ):
                self.activate = True
            else:
                self.activate = False

        self._handlers[MOUSEBUTTONDOWN].append(_mouse_button_down)

    def _text_input(self, event: pygame.event.Event):
        self._editing_text = ""
        self.text += event.text

    def _text_editing(self, event: pygame.event.Event):
        self._editing_text = event.text

    def _key_down(self, event: pygame.event.Event):
        if len(self._editing_text) > 0:
            return
        if event.key == K_BACKSPACE and len(self.text) > 0:
            self.text = self.text[:-1]
        elif event.key in [K_RETURN, K_KP_ENTER]:
            self.activate = False

    def _shift_in(self):
        assert self._visible == False

        self._visible = True

        def on_exit():
            self._visible_full = True

        self.activate = False
        self._flags["before_end"].clear()
        self._flags["before_end"].append(
            delayed_flag(
                self._flags["before_end"],
                lambda: blur_effect(
                    self._surface,
                    "linear",
                    (0, self._blur),
                    EFFECT_DURATION_MINI,
                ),
                EFFECT_DURATION_NORMAL - EFFECT_DURATION_MINI,
            )
        )
        self._flags["before_end"].append(
            alpha_effect(
                self._foreground, "ease_in", (0, 255), EFFECT_DURATION_NORMAL
            )
        )
        self._flags["before_end"].append(
            alpha_effect(
                self._background,
                "ease_in",
                (0, 50),
                EFFECT_DURATION_NORMAL,
                on_exit,
            )
        )

    def _shift_out(self):
        assert self._visible == True

        self._visible_full = False

        def on_exit():
            self._visible = False

        self.activate = False
        self._flags["before_end"].clear()
        self._flags["before_end"].append(
            blur_effect(
                self._surface,
                "linear",
                (self._blur, 0),
                EFFECT_DURATION_MINI,
            )
        )
        self._flags["before_end"].append(
            alpha_effect(
                self._foreground, "ease_out", (255, 0), EFFECT_DURATION_NORMAL
            )
        )
        self._flags["before_end"].append(
            alpha_effect(
                self._background,
                "ease_out",
                (self._background.get_alpha(), 0),
                EFFECT_DURATION_NORMAL,
                on_exit,
            )
        )

    @property
    def activate(self):
        return self._activate

    @activate.setter
    def activate(self, value: bool):
        if self._activate != value:
            if value:
                self._activate_in()
            else:
                self._activate_out()

    def _activate_in(self):
        assert self._visible == True
        assert self._activate == False

        self._activate = True

        play_sound("sound/sound1.ogg")

        def on_exit():
            pygame.key.start_text_input()
            pygame.key.set_text_input_rect(self._abs_rect)

            for event, handler in {
                (KEYDOWN, self._key_down),
                (TEXTINPUT, self._text_input),
                (TEXTEDITING, self._text_editing),
            }:
                if handler not in self._handlers[event]:
                    self._handlers[event].append(handler)
    
        self._flags["before_end"].clear()
        self._flags["before_end"].append(
            alpha_effect(
                self._background,
                "linear",
                (self._background.get_alpha(), 150),
                EFFECT_DURATION_TINY
                * (150 - self._background.get_alpha())
                / (150 - 50),
                on_exit
            )
        )

    def _activate_out(self):
        assert self._visible == True
        assert self._activate == True

        self._activate = False

        self._flags["before_end"].clear()
        self._flags["before_end"].append(
            alpha_effect(
                self._background,
                "linear",
                (self._background.get_alpha(), 50),
                EFFECT_DURATION_TINY
                * (self._background.get_alpha() - 50)
                / (150 - 50),
            )
        )

        for event, handler in {
            (KEYDOWN, self._key_down),
            (TEXTINPUT, self._text_input),
            (TEXTEDITING, self._text_editing),
        }:
            if handler in self._handlers[event]:
                self._handlers[event].remove(handler)

        pygame.key.stop_text_input()

    def _draw_begin(self) -> None:

        self._foreground.fill(COLOR_TRANSPARENT)
        pygame.draw.rect(
            self._foreground, (0, 0, 0, 80), self._foreground.get_rect(), 2
        )

        text_surface: pygame.Surface
        text_surface_rect: pygame.Rect

        if len(self.text) == 0 and len(self._editing_text) == 0:
            text_surface, text_surface_rect = TEXT_FONT.render(
                self.text_hint, (80, 80, 80), style=STYLE_UNDERLINE
            )
        else:
            text_surface, text_surface_rect = TEXT_FONT.render(self.text)
            if len(self._editing_text) > 0:
                editing_text_surface: pygame.Surface
                editing_text_surface_rect: pygame.Rect
                (
                    editing_text_surface,
                    editing_text_surface_rect,
                ) = TEXT_FONT.render(self._editing_text, style=STYLE_UNDERLINE)
                tmp = pygame.Surface(
                    (
                        text_surface_rect.width
                        + editing_text_surface_rect.width,
                        max(
                            text_surface_rect.height,
                            editing_text_surface_rect.height,
                        ),
                    ),
                    pygame.SRCALPHA,
                )
                tmp.blit(
                    text_surface,
                    (
                        0,
                        max(
                            editing_text_surface_rect.y - text_surface_rect.y,
                            0,
                        ),
                    ),
                )
                tmp.blit(
                    editing_text_surface,
                    (
                        text_surface_rect.width,
                        max(
                            text_surface_rect.y - editing_text_surface_rect.y,
                            0,
                        ),
                    ),
                )
                text_surface = tmp
                text_surface_rect = pygame.Rect(
                    text_surface_rect.x,
                    max(text_surface_rect.y, editing_text_surface_rect.y),
                    tmp.get_width(),
                    tmp.get_height(),
                )

        foreground_rect = self._foreground.get_rect()

        if foreground_rect.contains(
            text_surface.get_rect(midbottom=foreground_rect.midbottom).move(
                0,
                text_surface_rect.height
                - text_surface_rect.y
                - 0.2 * foreground_rect.height,
            )
        ):
            self._foreground.blit(
                text_surface,
                text_surface.get_rect(midbottom=foreground_rect.midbottom).move(
                    0,
                    text_surface_rect.height
                    - text_surface_rect.y
                    - 0.2 * foreground_rect.height,
                ),
            )
        else:
            self._foreground.blit(
                text_surface,
                text_surface.get_rect(
                    bottomright=foreground_rect.bottomright
                ).move(
                    0,
                    text_surface_rect.height
                    - text_surface_rect.y
                    - 0.2 * foreground_rect.height,
                ),
            )

    def _draw_end(self) -> None:
        if self._visible_full:
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

        if self._visible:
            self._surface.blit(self._background, (0, 0))
            self._surface.blit(self._foreground, (0, 0))
