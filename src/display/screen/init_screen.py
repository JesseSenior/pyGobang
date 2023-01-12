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
from pygame.locals import QUIT

import src.constants
from src.display.tool import play_sound
from src.display.screen import Screen
from src.constants import (
    SCREEN_CHANGE,
    WINDOW_SIZE,
    EFFECT_DURATION_MINI,
    EFFECT_DURATION_NORMAL,
)
from src.display.effect import (
    temporary_flag,
    delayed_flag,
    mosaic_effect,
    surface_mosaic,
)
from src.display.widget.background import Background
from src.display.widget.logo import LOGO


class InitScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self._game_logo = LOGO(
            self, self._surface.get_rect().center, 0.75, blink=False
        )
        self._sub_widgets.append(self._game_logo)

        if src.constants.GAME_BACKGROUND == None:
            src.constants.GAME_BACKGROUND = Background()
        src.constants.GAME_BACKGROUND.set_surface(
            self, self._surface.get_rect()
        )

        self._visible = False
        self.visible = True

        self._background_prepared = False

    def _draw_begin(self) -> None:
        src.constants.GAME_BACKGROUND.draw()
        if (
            self._background_prepared
            != src.constants.GAME_BACKGROUND.background_prepared
        ):
            self._background_prepared = (
                src.constants.GAME_BACKGROUND.background_prepared
            )
            self._flags["before_end"].append(
                delayed_flag(
                    self._flags["before_end"],
                    lambda: temporary_flag(
                        self,
                        lambda: pygame.event.post(
                            pygame.event.Event(SCREEN_CHANGE, screen=2)
                        ),
                    ),
                    EFFECT_DURATION_NORMAL * 2,
                )
            )

    def _shift_in(self):
        assert self._visible == False

        self._game_logo.visible = True

        self._visible = True

        self._flags["before_end"].append(
            mosaic_effect(
                self._surface,
                "ease_in",
                (min(WINDOW_SIZE) // 10, 1),
                EFFECT_DURATION_MINI,
            )
        )

    def _shift_out(self, event: pygame.event.Event = None):
        assert self._visible == True

        if event.type == QUIT:
            self._stop_loop = 0
            return

        self._game_logo.visible = False

        def on_exit(event):
            self._visible = False
            self._stop_loop = event.screen

        def delayed_shift():
            play_sound("sound/sound3.ogg")
            return mosaic_effect(
                self._surface,
                "ease_out",
                (1, min(WINDOW_SIZE) // 10),
                EFFECT_DURATION_MINI,
                on_exit=lambda: on_exit(event),
            )

        self._flags["before_end"].append(
            delayed_flag(
                self._flags["before_end"],
                delayed_shift,
                (EFFECT_DURATION_NORMAL - EFFECT_DURATION_MINI),
            )
        )

    def _draw_end(self) -> None:
        if not self.visible:
            self._surface.blit(
                surface_mosaic(self._surface, min(WINDOW_SIZE) // 10), (0, 0)
            )
