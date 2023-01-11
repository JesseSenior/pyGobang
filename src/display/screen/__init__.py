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

File: src/display/screen/__init__.py
Description: General definition of Screen.
"""

import pygame
from pygame.locals import QUIT
from typing import List, Tuple

global GAME_BACKGROUND
from src.constants import SCREEN_CHANGE, MAX_FPS, GAME_BACKGROUND
from src.display.widget import Widget


class Screen(Widget):
    """General game screen to the pyGobang GUI.

    Functions:
        __init__() -> None: Initialization to the screen.
        loop() -> None:
            Continuously updating surface of the screen, handling and operating
            events, until `_stop_loop` is set.
    """

    def __init__(self) -> None:
        """Initialization to the screen."""
        assert pygame.display.get_surface() != None

        super().__init__(None, pygame.display.get_surface().get_rect(), pygame.display.get_surface())
        self._clock = pygame.time.Clock()
        self._visible = False
        self._stop_loop = None

        self._handlers[QUIT].append(self._screen_chage)
        self._handlers[SCREEN_CHANGE].append(self._screen_chage)

    def _screen_chage(self, event: pygame.event.Event):
        self.visible=False,event

            
    @Widget.visible.setter
    def visible(self, value: bool or Tuple[bool, pygame.event.Event]):
        if type(value)==bool:
            if self._visible != value:
                if value:
                    self._shift_in()
                else:
                    self._shift_out()
        else:
            value,event=value
            if self._visible != value:
                if value:
                    self._shift_in()
                else:
                    self._shift_out(event)


    def _shift_out(self, event: pygame.event.Event = None):
        if event.type == QUIT:
            self._stop_loop = 0
        else:
            self._stop_loop = event.screen
        self._visible=False
    
    def loop(self):
        """Continuously updating surface of the screen, handling and operating
        events, until `_stop_loop` is set.
        """
        while True:
            for event in pygame.event.get():
                self._event_handler(event)
            if self._stop_loop != None:
                return self._stop_loop
            self.draw()
            pygame.display.update()
            self._clock.tick(MAX_FPS)


from src.display.screen.init_screen import InitScreen
from src.display.screen.main_screen import MainScreen
from src.display.screen.game_screen import GameScreen

screen_list: List[Screen]
screen_list = [None, InitScreen, MainScreen, GameScreen]
