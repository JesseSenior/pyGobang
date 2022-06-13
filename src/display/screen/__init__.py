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

global GAME_BACKGROUND
from src.constants import SCREEN_CHANGE, MAX_FPS, GAME_BACKGROUND
from src.display.widget import Widget


class Screen(Widget):
    def __init__(self) -> None:
        assert pygame.display.get_surface() != None

        super().__init__(None, None, pygame.display.get_surface())
        self._clock = pygame.time.Clock()

        self._handlers[QUIT].append(self._game_quit)
        self._handlers[SCREEN_CHANGE].append(self._screen_chage)

    def _game_quit(self, event: pygame.event.Event):
        print("✨愿你有一天能和你最重要的人重逢✨")
        self.stop_loop = 0

    def _screen_chage(self, event: pygame.event.Event):
        self.stop_loop = event.screen

    def loop(self):
        while True:
            for event in pygame.event.get():
                self.event_handler(event)
            if hasattr(self, "stop_loop"):
                return self.stop_loop
            self.draw()
            pygame.display.update()
            self._clock.tick(MAX_FPS)


from src.display.screen.init_screen import InitScreen
from src.display.screen.main_screen import MainScreen
from src.display.screen.game_screen import GameScreen

screen_list = [None, InitScreen, MainScreen, GameScreen]
