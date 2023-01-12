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

File: src/display/widget/table.py
Description: General list widget.
"""
from __future__ import annotations
import pygame
from pygame.constants import (
    MOUSEBUTTONDOWN,
    BUTTON_LEFT,
    BUTTON_WHEELDOWN,
    BUTTON_WHEELUP,
)
from typing import List

from src.display.widget import Widget
from src.display.tool import play_sound
from src.constants import (
    COLOR_RED,
    COLOR_TRANSPARENT,
    COLOR_WHITE,
    TEXT_FONT,
    EFFECT_DURATION_TINY,
    EFFECT_DURATION_NORMAL,
)
from src.display.effect import alpha_effect, blur_effect, surface_blur


class Table(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        text_list: List[List[str]] = [],
        present_number: int = 4,
    ) -> None:
        super().__init__(parent, rect, surface)
        self._blur = 50
        self._surface.set_alpha(0)
        self._surface_raw = pygame.Surface(
            self._surface.get_size()
        ).convert_alpha()
        self._surface_raw.set_alpha(0)
        self._visible = False
        self._present_number = present_number
        self._item_height = self._surface.get_size()[1] // self._present_number

        self.set_text_list(text_list)

        def _mouse_button_down(event: pygame.event.Event):
            if self._visible and len(self._sub_widgets) > 0:
                if (
                    self._abs_rect.collidepoint(event.pos)
                    and event.button == BUTTON_LEFT
                ):
                    y = (
                        event.pos[1] - self._surface.get_abs_offset()[1]
                    ) // self._item_height
                    if (
                        self._active_item != y + self._display_offset
                        and len(self._sub_widgets) > y + self._display_offset
                    ):
                        play_sound("sound/sound1.ogg")
                        self._sub_widgets[self._active_item].activate = False
                        self._active_item = y + self._display_offset
                        self._sub_widgets[self._active_item].activate = True
                        self._active_item_change()

        def _mouse_scroll(event: pygame.event.Event):
            if self._visible and len(self._sub_widgets) > 0:
                if self._abs_rect.collidepoint(event.pos):
                    if event.button == BUTTON_WHEELDOWN:
                        if self._display_offset + self._present_number < len(
                            self._sub_widgets
                        ):
                            self._display_offset += 1
                    elif event.button == BUTTON_WHEELUP:
                        if self._display_offset > 0:
                            self._display_offset -= 1

        self._handlers[MOUSEBUTTONDOWN].append(_mouse_button_down)
        self._handlers[MOUSEBUTTONDOWN].append(_mouse_scroll)

    def _active_item_change(self):
        pass

    def set_text_list(self, text_list: List[List[str]] = []) -> None:
        self._sub_widgets = []

        if len(text_list) > 0:
            for text in text_list:
                tmp = pygame.Surface(
                    (self._surface.get_size()[0], self._item_height)
                ).convert_alpha()
                self._sub_widgets.append(Table.Item(self, tmp, text))
            self._active_item = 0
            self._display_offset = 0
            self._sub_widgets[0].activate = True
        else:
            self._active_item = None
            self._display_offset = 0

    def _shift_in(self):
        assert self._visible == False

        def onexit():
            self._visible = True
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

        self._flags["after_begin"].append(
            blur_effect(
                self._surface,
                "ease_in",
                (0, self._blur),
                EFFECT_DURATION_NORMAL,
                onexit,
            )
        )
        self._flags["before_end"].append(
            alpha_effect(
                self._surface_raw, "ease_in", (0, 255), EFFECT_DURATION_NORMAL
            )
        )

    def _shift_out(self):
        assert self._visible == True

        self._visible = False

        self._flags["after_begin"].append(
            blur_effect(
                self._surface,
                "ease_out",
                (self._blur, 0),
                EFFECT_DURATION_NORMAL,
            )
        )
        self._flags["before_end"].append(
            alpha_effect(
                self._surface_raw, "ease_out", (255, 0), EFFECT_DURATION_NORMAL
            )
        )

    def _draw_begin(self) -> None:
        self._surface_raw.fill(COLOR_TRANSPARENT)
        pygame.draw.rect(
            self._surface_raw, (0, 0, 0, 100), self._surface_raw.get_rect(), 3
        )
        if self._visible:
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

    def _draw_end(self) -> None:
        try:
            for i in range(
                self._display_offset,
                self._display_offset + self._present_number,
            ):
                self._surface_raw.blit(
                    self._sub_widgets[i].surface,
                    (0, (i - self._display_offset) * self._item_height),
                )
        except:
            pass
        self._surface.blit(self._surface_raw, (0, 0))

    class Item(Widget):
        def __init__(
            self,
            parent: Widget,
            surface: pygame.Surface,
            text: List[str] = [""],
        ) -> None:
            super().__init__(parent, surface.get_rect(), surface)
            self._surface.fill(COLOR_TRANSPARENT)
            self._surface.set_alpha(255)
            self._outer_edge = 3
            self._text_size = (
                (surface.get_size()[1] - self._outer_edge) * 0.9 / len(text)
            )
            self._text_gap = (
                (surface.get_size()[1] - self._outer_edge)
                * 0.1
                / (len(text) + 1)
            )
            self._text = [
                (
                    TEXT_FONT.render(text[i], size=self._text_size)[0],
                    (
                        self._text_gap + self._outer_edge,
                        self._text_gap * (i + 1)
                        + self._text_size * i
                        + self._outer_edge,
                    ),
                )
                for i in range(len(text))
            ]
            self._active_background = pygame.Surface(
                self._surface.get_size()
            ).convert_alpha()
            self._active_background.fill(COLOR_WHITE)
            self._active_background.set_alpha(50)
            self._activate = False

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
            assert self._activate == False
            self._activate = True

            self._flags["before_end"].clear()
            current_alpha = self._active_background.get_alpha()
            self._flags["before_end"].append(
                alpha_effect(
                    self._active_background,
                    "linear",
                    (current_alpha, 150),
                    EFFECT_DURATION_TINY * (150 - current_alpha) / 150,
                )
            )

        def _activate_out(self):
            assert self._activate == True

            self._activate = False

            self._flags["before_end"].clear()
            current_alpha = self._active_background.get_alpha()
            self._flags["before_end"].append(
                alpha_effect(
                    self._active_background,
                    "linear",
                    (current_alpha, 50),
                    EFFECT_DURATION_TINY * (current_alpha - 50) / 150,
                )
            )

        def _draw_begin(self) -> None:
            self._surface.fill(COLOR_TRANSPARENT)

        def _draw_end(self) -> None:
            self._surface.blit(self._active_background, (0, 0))
            if self._activate:
                pygame.draw.rect(
                    self._surface,
                    (*COLOR_RED, 150),
                    self._surface.get_rect(),
                    2,
                )
            else:
                pygame.draw.rect(
                    self._surface,
                    (0, 0, 0, 80),
                    self._surface.get_rect(),
                    1,
                )
            for text, pos in self._text:
                self._surface.blit(text, pos)
