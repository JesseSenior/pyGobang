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

File: src/display/screen/init_screen.py
Description: The initial screen of the game.
"""
import pygame

import src.constants
from src.display.screen import Screen
from src.constants import SCREEN_CHANGE, WINDOW_SIZE
from src.display.effect import Flag, delayed_flag, mosaic_effect, surface_mosaic
from src.display.widget import Widget
from src.display.widget.background import Background
from src.display.widget.logo import LOGO


class InitScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self._game_logo = LOGO(self, self._surface.get_rect().center, 0.75)
        self._sub_widgets.append(self._game_logo)

        if src.constants.GAME_BACKGROUND == None:
            src.constants.GAME_BACKGROUND = Background()
        src.constants.GAME_BACKGROUND.set_surface(
            self, self._surface.get_rect()
        )

        self._visible = False
        self.visible = True
        self._flags.append(
            delayed_flag(self._flags, lambda: self.goto_main_screen(self), 3)
        )

    class goto_main_screen(Flag):
        def __init__(self, parent, on_exit=None) -> None:
            super().__init__(parent, on_exit)

        def execute(self) -> None:
            self._parent.visible = False
            self.exit()

    def draw_begin(self) -> None:
        src.constants.GAME_BACKGROUND.draw()

    @Widget.visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self.shift_in()
            else:
                self.shift_out()

    def shift_in(self):
        assert self._visible == False

        self._game_logo.visible = True

        self._visible = True

    def shift_out(self):
        assert self._visible == True

        self._game_logo.visible = False

        def onexit():
            self._visible = False
            pygame.event.post(pygame.event.Event(SCREEN_CHANGE, screen=2))

        self._flags.append(
            delayed_flag(
                self._flags,
                lambda: mosaic_effect(
                    self._surface,
                    "ease_out",
                    (1, min(WINDOW_SIZE) // 10),
                    1,
                    on_exit=onexit,
                ),
                1,
            )
        )

    def draw_end(self) -> None:
        if not self.visible:
            self._surface.blit(
                surface_mosaic(self._surface, min(WINDOW_SIZE) // 10), (0, 0)
            )
