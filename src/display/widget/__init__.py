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

File: src/display/widget/__init__.py
Description: General definition of Widget.
"""
from __future__ import annotations
import pygame
from collections import defaultdict
from typing import List


class Widget:
    """General widget to the pyGobang GUI.

    Attributes:
        parent (Widget): The widget's parent.
        rect (pygame.Rect): The widget's surface rect from its parent.
        surface (pygame.Surface): The widget's surface.
        visible (bool): Visibility of the widget.

    Functions:
        __init__() -> None: Initialization to the widget.
        draw() -> None: Draw widget to the surface.
    """

    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        subsurface: bool = True,
    ) -> None:
        """Initialization to the widget.

        Args:
            parent (Widget): The widget's parent.
            rect (pygame.Rect): The widget's surface rect from its parent.
            surface (pygame.Surface, optional):
                The widget's surface. Defaults to The subsurface from its parent
                according to the given rect. Overwrite this ONLY IF you want to
                use custom parent surface!
            subsurface (bool, optional):
                Whether to use a subsurface. Defaults to `True`. If arg
                `surface` is set, this arg will be ignored.
        """
        self._parent = parent

        if surface != None:
            self._surface = surface
        elif subsurface:
            self._surface = parent.surface.subsurface(rect)
        else:
            self._surface = pygame.Surface(rect.size)

        self._rect = rect

        if self._parent != None:
            self._abs_rect = pygame.Rect(
                self._parent.abs_rect.move(*self._rect.topleft).topleft,
                self._rect.size,
            )
        else:
            self._abs_rect=self._rect
        self._sub_widgets: List[Widget]
        self._sub_widgets = list()
        self._handlers = defaultdict(list)
        self._flags = {
            "before_begin": list(),
            "after_begin": list(),
            "before_end": list(),
            "after_end": list(),
        }
        self._visible = True

    @property
    def parent(self) -> Widget:
        """The widget's parent.

        Returns:
            Widget: The widget's parent.
        """
        return self._parent

    @property
    def rect(self) -> pygame.Rect:
        """The widget's surface rect from its parent.

        Returns:
            pygame.Rect: The widget's surface rect from its parent.
        """
        return self._rect

    @property
    def abs_rect(self) -> pygame.Rect:
        """The widget's surface absolute rect from Screen.

        Returns:
            pygame.Rect: The widget's surface absolute rect from Screen.
        """
        return self._abs_rect

    @property
    def surface(self) -> pygame.Surface:
        """Surface to the widget.

        Returns:
            pygame.Surface: Surface to the widget.
        """
        return self._surface

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self._shift_in()
            else:
                self._shift_out()

    def _shift_in(self):
        self._visible = True
        for sub_widget in self._sub_widgets:
            sub_widget.visible = True

    def _shift_out(self):
        for sub_widget in self._sub_widgets:
            sub_widget.visible = False
        self._visible = False

    def _event_handler(self, event: pygame.event.Event) -> None:
        """Event handler to the widget.

        Args:
            event (pygame.event.Event): Event
        """
        for handler in self._handlers[event.type]:
            handler(event)
        for sub_widget in self._sub_widgets:
            sub_widget._event_handler(event)

    def draw(self) -> None:
        """Default draw function to the widget.

        Notice:
            If you want to overwrite it,you MUST understand what you're doing!
        """
        self._process_flags(self._flags["before_begin"])
        self._draw_begin()
        self._process_flags(self._flags["after_begin"])
        self._draw_sub_widgets()
        self._process_flags(self._flags["before_end"])
        self._draw_end()
        self._process_flags(self._flags["after_end"])

    def _draw_begin(self) -> None:
        pass

    def _draw_sub_widgets(self, sub_widgets_list: list = None) -> None:
        if sub_widgets_list == None:
            for sub_widget in self._sub_widgets:
                sub_widget.draw()
        else:
            for sub_widget in sub_widgets_list:
                sub_widget.draw()

    def _process_flags(self, flag_list: list) -> None:
        for flag in flag_list:
            if not flag.is_finished:
                flag.execute()
            else:
                flag_list.remove(flag)

    def _draw_end(self) -> None:
        pass
