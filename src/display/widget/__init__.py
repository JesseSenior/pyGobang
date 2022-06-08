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


class Widget:
    """General widget to the GUI.
    """

    def __init__(
        self, parent: Widget, rect: pygame.Rect, surface: pygame.Surface = None
    ) -> None:
        """Initialization to the widget.

        Args:
            parent (Widget): The widget's parent.
            rect (pygame.Rect): The widget's surface rect from its parent.
            surface (pygame.Surface, optional): 
                The widget's surface. Defaults to The subsurface from its parent
                according to the given rect. NOT RECOMMEND TO OVERWRITE!
        """
        self._parent = parent
        self._surface = (
            parent.surface.subsurface(rect) if surface == None else surface
        )
        self._sub_widgets = list()
        self._handlers = defaultdict(list)
        self._pre_flags = list()
        self._flags = list()
        self._visible = True

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
        self._visible = value

    def event_handler(self, event: pygame.event.Event):
        """Event handler to the widget.

        Args:
            event (pygame.event.Event): Event
        """
        for handler in self._handlers[event.type]:
            handler(event)
        for sub_widget in self._sub_widgets:
            sub_widget.event_handler(event)

    def draw(self) -> None:
        """Default draw function to the widget.
        
        Notice:
            If you want to overwrite it,you MUST understand what you're doing!
        """
        self.draw_begin()
        self.process_flags(self._pre_flags)
        self.draw_sub_widgets()
        self.process_flags()
        self.draw_end()

    def draw_begin(self) -> None:
        pass

    def draw_sub_widgets(self, sub_widgets_list: list = None) -> None:
        for sub_widget in (
            self._sub_widgets if sub_widgets_list == None else sub_widgets_list
        ):
            sub_widget.draw()

    def process_flags(self, flag_list: list = None) -> None:
        if flag_list == None:
            flag_list = self._flags
        for flag in flag_list:
            if not flag.is_finished:
                flag.execute()
            else:
                flag_list.remove(flag)

    def draw_end(self) -> None:
        pass

    def __del__(self) -> None:
        pass
