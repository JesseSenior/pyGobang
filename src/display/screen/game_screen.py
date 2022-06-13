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

File: src/display/screen/game_screen.py
Description: The primary game screen of the game.
"""
from math import ceil
import time
import pygame

import src.constants
from src.constants import (
    COLOR_BLACK,
    COLOR_RED,
    COLOR_TRANSPARENT,
    COLOR_WHITE,
    DATABASE,
    SCREEN_CHANGE,
    TIME_FORMAT,
    WINDOW_SIZE,
)
from src.core import Board
from src.display.effect import (
    alpha_effect,
    delayed_flag,
    mosaic_effect,
    surface_mosaic,
    temporary_flag,
)
from src.display.screen import Screen
from src.display.widget import Widget
from src.display.widget.board import BoardUI, HumanUIPlayer, RobotUIPlayer
from src.display.widget.button import Button
from src.display.widget.input_box import InputBox
from src.display.widget.text import Text


class GameScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        src.constants.GAME_BACKGROUND.set_surface(
            self, self._surface.get_rect()
        )
        self._visible = False
        if src.constants.LAST_BOARD == None:
            self._init_game_mode()
        else:
            self._game_mode = 0
            self._board = src.constants.LAST_BOARD
            self._board.timestamp = time.strftime(
                TIME_FORMAT, time.localtime(time.time())
            )
            src.constants.LAST_BOARD = None
            self._init_gameboard()
        self.visible = True

    def _init_game_mode(self) -> None:
        self._game_mode = 0

        def set_game_mode(mode: int):
            """set game mode.

            Args:
                mode (int): The gamemode id. 0 is PVP, 1 is PVE.
            """
            self._game_mode = mode
            self._game_mode_pvp_button.visible = False
            self._game_mode_pve_button.visible = False
            self._return_button.visible = False

            def onexit():
                self._sub_widgets.remove(self._game_mode_pvp_button)
                self._sub_widgets.remove(self._game_mode_pve_button)
                self._sub_widgets.remove(self._return_button)
                del self._game_mode_pvp_button
                del self._game_mode_pve_button
                del self._return_button
                self._init_player()

            self._flags.append(
                delayed_flag(
                    self._flags, lambda: temporary_flag(self, onexit), 1
                )
            )

        self._game_mode_pvp_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] * 5 / 13 / 2,
                WINDOW_SIZE[1] / 2
                - WINDOW_SIZE[1] / 13 / 2
                - WINDOW_SIZE[1] * 2 / 13,
                WINDOW_SIZE[0] * 5 / 13,
                WINDOW_SIZE[1] / 13,
            ),
            text="人人对战",
            on_press=lambda: set_game_mode(0),
        )
        self._game_mode_pvp_button.visible = True
        self._sub_widgets.append(self._game_mode_pvp_button)

        self._game_mode_pve_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] * 5 / 13 / 2,
                WINDOW_SIZE[1] / 2 - WINDOW_SIZE[1] / 13 / 2,
                WINDOW_SIZE[0] * 5 / 13,
                WINDOW_SIZE[1] / 13,
            ),
            text="人机对战",
            on_press=lambda: set_game_mode(1),
        )
        self._game_mode_pve_button.visible = True
        self._sub_widgets.append(self._game_mode_pve_button)

        self._return_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] * 5 / 13 / 2,
                WINDOW_SIZE[1] / 2
                - WINDOW_SIZE[1] / 13 / 2
                + WINDOW_SIZE[1] * 2 / 13,
                WINDOW_SIZE[0] * 5 / 13,
                WINDOW_SIZE[1] / 13,
            ),
            text="返回主界面",
            on_press=lambda: pygame.event.post(
                pygame.event.Event(SCREEN_CHANGE, screen=2)
            ),
        )
        self._return_button.visible = True
        self._sub_widgets.append(self._return_button)

    def _init_player(self):
        self._board = None

        self._player_A_name_input_box = InputBox(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] * 5 / 13 / 2,
                WINDOW_SIZE[1] / 2
                - WINDOW_SIZE[1] / 13 / 2
                - WINDOW_SIZE[1] * 3 / 13,
                WINDOW_SIZE[0] * 5 / 13,
                WINDOW_SIZE[1] / 13,
            ),
            text_hint="先手玩家名",
        )
        self._player_A_name_input_box.visible = True
        self._sub_widgets.append(self._player_A_name_input_box)

        if self._game_mode == 0:
            self._player_B_name_input_box = InputBox(
                self,
                pygame.Rect(
                    WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] * 5 / 13 / 2,
                    WINDOW_SIZE[1] / 2
                    - WINDOW_SIZE[1] / 13 / 2
                    - WINDOW_SIZE[1] * 1 / 13,
                    WINDOW_SIZE[0] * 5 / 13,
                    WINDOW_SIZE[1] / 13,
                ),
                text_hint="后手玩家名",
            )
            self._player_B_name_input_box.visible = True
            self._sub_widgets.append(self._player_B_name_input_box)

        def set_player_name():
            self._board = Board(
                (9, 9) if self._game_mode else src.constants.DEFAULT_BOARD_SIZE,
                competitor_black=self._player_A_name_input_box.text,
                competitor_white=self._player_B_name_input_box.text
                if self._game_mode == 0
                else "AI",
            )

            if self._game_mode == 0:
                self._player_B_name_input_box.visible = False
            self._player_A_name_input_box.visible = False
            self._finish_button.visible = False
            self._return_button.visible = False

            def onexit():
                self._sub_widgets.remove(self._player_A_name_input_box)
                if self._game_mode == 0:
                    self._sub_widgets.remove(self._player_B_name_input_box)
                self._sub_widgets.remove(self._finish_button)
                self._sub_widgets.remove(self._return_button)
                if self._game_mode == 0:
                    del self._player_B_name_input_box
                del (
                    self._player_A_name_input_box,
                    self._finish_button,
                    self._return_button,
                )
                self._init_gameboard()

            self._flags.append(
                delayed_flag(
                    self._flags, lambda: temporary_flag(self, onexit), 1
                )
            )

        self._finish_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] * 5 / 13 / 2,
                WINDOW_SIZE[1] / 2
                - WINDOW_SIZE[1] / 13 / 2
                + WINDOW_SIZE[1] * 1 / 13,
                WINDOW_SIZE[0] * 5 / 13,
                WINDOW_SIZE[1] / 13,
            ),
            text="确定",
            on_press=set_player_name,
        )
        self._finish_button.visible = True
        self._sub_widgets.append(self._finish_button)

        self._return_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] / 2 - WINDOW_SIZE[0] * 5 / 13 / 2,
                WINDOW_SIZE[1] / 2
                - WINDOW_SIZE[1] / 13 / 2
                + WINDOW_SIZE[1] * 3 / 13,
                WINDOW_SIZE[0] * 5 / 13,
                WINDOW_SIZE[1] / 13,
            ),
            text="返回主界面",
            on_press=lambda: pygame.event.post(
                pygame.event.Event(SCREEN_CHANGE, screen=2)
            ),
        )
        self._return_button.visible = True
        self._sub_widgets.append(self._return_button)

    def _init_gameboard(self):
        self._boardUI = BoardUI(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.25 // 5,
                WINDOW_SIZE[1] * 0.5 // 5,
                min(WINDOW_SIZE) * 4 // 5,
                min(WINDOW_SIZE) * 4 // 5,
            ),
            board=self._board,
            player_list=[
                HumanUIPlayer,
                HumanUIPlayer if self._game_mode == 0 else RobotUIPlayer,
            ],
        )
        self._boardUI.visible = True
        self._sub_widgets.append(self._boardUI)

        def save_and_exit():
            DATABASE.append(self._board)
            pygame.event.post(pygame.event.Event(SCREEN_CHANGE, screen=2))

        self._save_and_exit_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.5 // 5 + min(WINDOW_SIZE) * 4 // 5,
                WINDOW_SIZE[1] // 13,
                WINDOW_SIZE[0] * 4.25 // 5 - min(WINDOW_SIZE) * 4 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="保存并退出",
            on_press=save_and_exit,
        )
        self._save_and_exit_button.visible = True
        self._sub_widgets.append(self._save_and_exit_button)

        self._exit_without_save_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.5 // 5 + min(WINDOW_SIZE) * 4 // 5,
                WINDOW_SIZE[1] * 3 // 13,
                WINDOW_SIZE[0] * 4.25 // 5 - min(WINDOW_SIZE) * 4 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="不保存并退出",
            on_press=lambda: pygame.event.post(
                pygame.event.Event(SCREEN_CHANGE, screen=2)
            ),
        )
        self._exit_without_save_button.visible = True
        self._sub_widgets.append(self._exit_without_save_button)

        def cancel():
            if self._game_mode == 0:
                self._boardUI.cancel(1)
            elif type(self._boardUI._player) == HumanUIPlayer:
                self._boardUI.cancel(2)

        self._cancel_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 4.75 // 5 - min(WINDOW_SIZE) * 1.5 // 10,
                WINDOW_SIZE[1] * 0.5 // 5
                + min(WINDOW_SIZE) * 4 // 5
                - min(WINDOW_SIZE) // 10,
                min(WINDOW_SIZE) * 1.5 // 10,
                min(WINDOW_SIZE) // 10,
            ),
            text="撤销",
            on_press=cancel,
        )

        self._cancel_button.visible = True
        self._sub_widgets.append(self._cancel_button)

        self._piece_status = PieceStatus(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.5 // 5 + min(WINDOW_SIZE) * 4 // 5,
                WINDOW_SIZE[1] * 0.5 // 5
                + min(WINDOW_SIZE) * 4 // 5
                - min(WINDOW_SIZE) // 10,
                min(WINDOW_SIZE) // 10,
                min(WINDOW_SIZE) // 10,
            ),
            board=self._board,
        )
        self._piece_status.visible = True
        self._sub_widgets.append(self._piece_status)

        self._piece_status_text = Text(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.5 // 5 + min(WINDOW_SIZE) * 4 // 5,
                WINDOW_SIZE[1] * 0.5 // 5
                + min(WINDOW_SIZE) * 2.75 // 5
                - min(WINDOW_SIZE) // 10,
                min(WINDOW_SIZE) * 2 // 5,
                min(WINDOW_SIZE) // 10,
            ),
            text="当前执子：",
        )
        self._piece_status_text.visible = True
        self._sub_widgets.append(self._piece_status_text)

        self._current_player_text = Text(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.5 // 5 + min(WINDOW_SIZE) * 4 // 5,
                WINDOW_SIZE[1] * 0.5 // 5
                + min(WINDOW_SIZE) * 3.25 // 5
                - min(WINDOW_SIZE) // 10,
                min(WINDOW_SIZE) * 2 // 5,
                min(WINDOW_SIZE) // 10,
            ),
            text="",
        )
        self._current_player_text.visible = True
        self._sub_widgets.append(self._current_player_text)

    def draw_begin(self) -> None:
        if self._visible:
            src.constants.GAME_BACKGROUND.draw()
        if hasattr(self, "_current_player_text"):
            self._piece_status_text.text = "当前执子："
            self._current_player_text.text = [
                self._board.competitor_black,
                self._board.competitor_white,
            ][self._board.current_side]
            if self._board.winner != None:
                self._piece_status_text.text = "胜利者："
                self._current_player_text.text = [
                    self._board.competitor_black,
                    self._board.competitor_white,
                ][self._board.winner]

    def draw_end(self) -> None:
        if not self.visible:
            self._surface.blit(
                surface_mosaic(self._surface, min(WINDOW_SIZE) // 10), (0, 0)
            )

    @Widget.visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self.shift_in()
            else:
                self.shift_out()

    def shift_in(self):
        assert self._visible == False

        self._visible = True

        self._flags.append(
            mosaic_effect(
                self._surface, "ease_in", (min(WINDOW_SIZE) // 10, 1), 1
            )
        )

    def shift_out(self, event: pygame.event.Event):
        assert self._visible == True

        for widget in self._sub_widgets:
            try:
                widget.visible = False
            except:
                pass

        def onexit(event):
            self._visible = False
            self.stop_loop = event.screen

        self._flags.append(
            mosaic_effect(
                self._surface,
                "ease_out",
                (1, min(WINDOW_SIZE) // 10),
                1,
                on_exit=lambda: onexit(event),
            )
        )

    def _screen_chage(self, event: pygame.event.Event):
        self.shift_out(event)


class PieceStatus(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        board: Board = None,
    ) -> None:
        super().__init__(parent, rect, surface)
        self._board = board
        self._status = self._board.current_side
        self._radius = min(self._surface.get_size()) / 2
        self._surface_raw = [
            pygame.Surface(self._surface.get_size()).convert_alpha(),
            pygame.Surface(self._surface.get_size()).convert_alpha(),
        ]
        self._surface_raw[0].fill(COLOR_TRANSPARENT)
        self._surface_raw[1].fill(COLOR_TRANSPARENT)
        self._surface_raw[self._status].set_alpha(255)
        self._surface_raw[1 - self._status].set_alpha(0)
        pygame.draw.circle(
            self._surface_raw[0],
            COLOR_BLACK,
            self._surface_raw[0].get_rect().center,
            self._radius,
        )
        pygame.draw.circle(
            self._surface_raw[0],
            COLOR_WHITE,
            self._surface_raw[0].get_rect().center,
            self._radius,
            ceil(self._radius / 20),
        )
        pygame.draw.circle(
            self._surface_raw[1],
            COLOR_WHITE,
            self._surface_raw[1].get_rect().center,
            self._radius,
        )
        pygame.draw.circle(
            self._surface_raw[1],
            COLOR_BLACK,
            self._surface_raw[1].get_rect().center,
            self._radius,
            ceil(self._radius / 20),
        )

        self._surface_raw_final = pygame.Surface(
            self._surface.get_size()
        ).convert_alpha()
        self._surface_raw_final.fill(COLOR_TRANSPARENT)
        self._surface_raw_final.set_alpha(0)
        self._visible = False

    def draw_begin(self) -> None:
        status = (
            self._status if self._board.winner == None else self._board.winner
        )
        if self._status != status:
            self._flags.append(
                alpha_effect(
                    self._surface_raw[1 - status], "ease_in_out", (255, 0), 0.2
                )
            )
            self._flags.append(
                alpha_effect(
                    self._surface_raw[status], "ease_in_out", (0, 255), 0.2
                )
            )
            self._status = status

    def draw_end(self) -> None:
        self._surface_raw_final.fill(COLOR_TRANSPARENT)
        self._surface_raw_final.blit(self._surface_raw[0], (0, 0))
        self._surface_raw_final.blit(self._surface_raw[1], (0, 0))
        if self._board.winner != None:
            pygame.draw.circle(
                self._surface_raw_final,
                COLOR_RED,
                self._surface_raw_final.get_rect().center,
                self._radius,
                ceil(self._radius / 5),
            )
        self._surface.blit(self._surface_raw_final, (0, 0))

    @Widget.visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self.shift_in()
            else:
                self.shift_out()

    def shift_in(self):
        assert self._visible == False

        self._visible = True

        self._flags.append(
            alpha_effect(self._surface_raw_final, "ease_in", (0, 255), 1)
        )

    def shift_out(self):
        assert self._visible == True

        self._visible = False

        self._flags.append(
            alpha_effect(self._surface_raw_final, "ease_out", (255, 0), 1)
        )

