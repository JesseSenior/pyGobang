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
from src.constants import COLOR_RED, COLOR_TRANSPARENT, TEXT_FONT
from src.display.effect import alpha_effect, blur_effect, surface_blur


class Table(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        text_list: List[str] = [],
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
                    pygame.Rect(
                        *self._surface.get_abs_offset(),
                        *self._surface.get_size()
                    ).collidepoint(event.pos)
                    and event.button == BUTTON_LEFT
                ):
                    y = (
                        event.pos[1] - self._surface.get_abs_offset()[1]
                    ) // self._item_height
                    if (
                        self._active_item != y + self._display_offset
                        and len(self._sub_widgets) > y + self._display_offset
                    ):
                        self._sub_widgets[self._active_item].active = False
                        self._active_item = y + self._display_offset
                        self._sub_widgets[self._active_item].active = True

        def _mouse_scroll(event: pygame.event.Event):
            if self._visible and len(self._sub_widgets) > 0:
                if pygame.Rect(
                    *self._surface.get_abs_offset(), *self._surface.get_size()
                ).collidepoint(event.pos):
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

    def set_text_list(self, text_list: List[str] = []) -> None:
        self._sub_widgets = []
        self._sub_widgets_surface = []

        def make_surface():
            tmp = pygame.Surface(
                (self._surface.get_size()[0], self._item_height)
            ).convert_alpha()
            self._sub_widgets_surface.append(tmp)
            return tmp

        for text in text_list:
            self._sub_widgets.append(Table.Item(self, make_surface(), text))
        if len(text_list) > 0:
            self._active_item = 0
            self._display_offset = 0
            self._sub_widgets[0].active = True
            for widget in self._sub_widgets:
                widget.visible = True
        else:
            self._active_item = None
            self._display_offset = 0

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

        self._pre_flags.append(
            blur_effect(
                self._surface, "ease_in", (0, self._blur), duration, onexit
            )
        )
        self._flags.append(
            alpha_effect(self._surface_raw, "ease_in", (0, 255), duration)
        )

    def shift_out(self, duration: float):
        assert self._visible == True

        self._visible = False

        self._pre_flags.append(
            blur_effect(self._surface, "ease_out", (self._blur, 0), duration)
        )
        self._flags.append(
            alpha_effect(self._surface_raw, "ease_out", (255, 0,), duration)
        )

    def draw_begin(self) -> None:
        self._surface_raw.fill(COLOR_TRANSPARENT)
        pygame.draw.rect(
            self._surface_raw, (0, 0, 0, 100), self._surface_raw.get_rect(), 3
        )
        if self._visible == True:
            self._surface.blit(surface_blur(self._surface, self._blur), (0, 0))

    def draw_end(self) -> None:
        try:
            for i in range(
                self._display_offset,
                self._display_offset + self._present_number,
            ):
                self._surface_raw.blit(
                    self._sub_widgets_surface[i],
                    (0, (i - self._display_offset) * self._item_height),
                )
        except:
            pass
        self._surface.blit(self._surface_raw, (0, 0))

    class Item(Widget):
        def __init__(
            self, parent: Widget, surface: pygame.Surface, text: str = ""
        ) -> None:
            super().__init__(parent, surface.get_rect(), surface)
            self._surface.fill(COLOR_TRANSPARENT)
            self._surface.set_alpha(0)
            self._text = TEXT_FONT.render(
                text, size=min(surface.get_size()) // 2.5
            )[0]
            self._visible = False
            self._active = False

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
                alpha_effect(
                    self._surface, "ease_in", (0, 255), duration, onexit
                )
            )

        def shift_out(self, duration: float):
            assert self._visible == True

            def onexit():
                self._visible = False

            self._flags.append(
                alpha_effect(
                    self._surface, "ease_out", (255, 0), duration, onexit
                )
            )

        @property
        def active(self):
            return self._active

        @active.setter
        def active(self, value: bool):
            self._active = value

        def draw_begin(self) -> None:
            self._surface.fill(COLOR_TRANSPARENT)
            if self._active:
                pygame.draw.rect(
                    self._surface, (*COLOR_RED, 80), self._surface.get_rect(), 1
                )
            else:
                pygame.draw.rect(
                    self._surface, (0, 0, 0, 40), self._surface.get_rect(), 1
                )

        def draw_end(self) -> None:
            self._surface.blit(
                self._text,
                (self._text.get_size()[1] // 5, self._text.get_size()[1] // 5),
            )
            self._surface.blit(
                self._text,
                (
                    self._text.get_size()[1] // 5,
                    self._text.get_size()[1]
                    + self._text.get_size()[1] * 2 // 5,
                ),
                pygame.Rect(
                    self._surface.get_size()[0]
                    - self._text.get_size()[1] * 2 // 5,
                    0,
                    *self._text.get_size()
                ),
            )

