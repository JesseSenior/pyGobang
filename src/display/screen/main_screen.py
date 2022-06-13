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

File: src/display/screen/main_screen.py
Description: The main screen of the game.
"""
import pygame
from pygame.constants import QUIT
from collections import defaultdict

import src.constants
from src.constants import (
    DATABASE,
    SCREEN_CHANGE,
    WINDOW_SIZE,
)
from src.core import Board
from src.display.effect import mosaic_effect, surface_mosaic
from src.display.screen import Screen
from src.display.widget import Widget
from src.display.widget.board import BoardUI, MonkeyUIPlayer
from src.display.widget.button import Button
from src.display.widget.input_box import InputBox
from src.display.widget.logo import LOGO
from src.display.widget.table import Table
from src.display.widget.text import Text


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self._visible = False
        src.constants.GAME_BACKGROUND.set_surface(
            self, self._surface.get_rect()
        )

        self._game_logo = LOGO(
            self,
            (
                WINDOW_SIZE[0] * 0.5 // 5 + min(WINDOW_SIZE) * 2.5 // 5 // 2,
                WINDOW_SIZE[1] * 2.5 // 13,
            ),
            0.5,
        )
        self._game_logo.visible = True
        self._sub_widgets.append(self._game_logo)

        self._board = BoardUI(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.5 // 5,
                WINDOW_SIZE[1] * 1.75 // 5,
                min(WINDOW_SIZE) * 2.75 // 5,
                min(WINDOW_SIZE) * 2.75 // 5,
            ),
            player_list=[MonkeyUIPlayer, MonkeyUIPlayer],
        )
        self._board.visible = True
        self._sub_widgets.append(self._board)

        self._main_list = []
        self._start_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="开始游戏",
            on_press=lambda: pygame.event.post(
                pygame.event.Event(SCREEN_CHANGE, screen=3)
            ),
        )
        self._sub_widgets.append(self._start_button)
        self._main_list.append(self._start_button)
        self._current_list = self._main_list

        def return_button():
            for widget in self._current_list:
                widget.visible = False
            for widget in self._main_list:
                widget.visible = True
            if self._current_list == self._history_list:
                self._board.editable = True
                self._board.set_player_list(self._board._player_list)
            self._current_list = self._main_list

        self._history_list = []

        def history_button():
            for widget in self._main_list:
                widget.visible = False
            for widget in self._history_list:
                widget.visible = True
            self._current_list = self._history_list

        self._history_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 3 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="历史对战",
            on_press=history_button,
        )
        self._sub_widgets.append(self._history_button)
        self._main_list.append(self._history_button)

        self._statistic_list = []

        def statistic_button():
            for widget in self._main_list:
                widget.visible = False
            for widget in self._statistic_list:
                widget.visible = True
            self._current_list = self._statistic_list

        self._statistic_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 5 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="统计信息",
            on_press=statistic_button,
        )
        self._sub_widgets.append(self._statistic_button)
        self._main_list.append(self._statistic_button)

        self._setting_list = []

        def setting_button():
            for widget in self._main_list:
                widget.visible = False
            for widget in self._setting_list:
                widget.visible = True
            self._current_list = self._setting_list

        self._setting_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 7 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="设置",
            on_press=setting_button,
        )
        self._sub_widgets.append(self._setting_button)
        self._main_list.append(self._setting_button)

        self._about_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 9 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="关于",
            on_press=lambda: print("作者是Jesse Senior~"),
        )
        self._sub_widgets.append(self._about_button)
        self._main_list.append(self._about_button)

        self._exit_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 11 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="退出",
            on_press=lambda: pygame.event.post(pygame.event.Event(QUIT)),
        )
        self._sub_widgets.append(self._exit_button)
        self._main_list.append(self._exit_button)

        self._return_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="返回",
            on_press=return_button,
        )
        self._sub_widgets.append(self._return_button)
        self._history_list.append(self._return_button)
        self._statistic_list.append(self._return_button)
        self._setting_list.append(self._return_button)

        self._history_table = MainScreen.history_table(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 3 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 7 // 13,
            ),
            present_number=7,
        )
        self._sub_widgets.append(self._history_table)
        self._history_list.append(self._history_table)

        def review_button():
            if len(self._history_table._boards) > 0:
                src.constants.LAST_BOARD = self._history_table._boards[
                    self._history_table._active_item
                ]
                pygame.event.post(pygame.event.Event(SCREEN_CHANGE, screen=3))

        self._review_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 11 // 13,
                WINDOW_SIZE[0] * 0.6 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="恢复",
            on_press=review_button,
        )
        self._sub_widgets.append(self._review_button)
        self._history_list.append(self._review_button)

        def delete_button():
            if len(self._history_table._boards) > 0:
                DATABASE.erase(
                    self._history_table._boards[
                        self._history_table._active_item
                    ].timestamp
                )
                self._board.load_board(Board())
                self._history_table.refresh()

        self._delete_button = Button(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3.9 // 5,
                WINDOW_SIZE[1] * 11 // 13,
                WINDOW_SIZE[0] * 0.6 // 5,
                WINDOW_SIZE[1] // 13,
            ),
            text="删除",
            on_press=delete_button,
        )
        self._sub_widgets.append(self._delete_button)
        self._history_list.append(self._delete_button)

        self._statistic_table = MainScreen.statistic_table(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 3 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 9 // 13,
            ),
            present_number=9,
        )
        self._sub_widgets.append(self._statistic_table)
        self._statistic_list.append(self._statistic_table)

        self._setting_board_size_text = Text(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 3 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 1 // 13,
            ),
            text="棋盘尺寸:",
        )
        self._sub_widgets.append(self._setting_board_size_text)
        self._setting_list.append(self._setting_board_size_text)

        self._setting_board_size_inputbox = MainScreen.setting_board_size_inputbox(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 4 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 1 // 13,
            ),
            text_hint=str(src.constants.DEFAULT_BOARD_SIZE),
        )
        self._sub_widgets.append(self._setting_board_size_inputbox)
        self._setting_list.append(self._setting_board_size_inputbox)

        self._setting_gentexture_speed_text = Text(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 5 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 1 // 13,
            ),
            text="纹理质量:",
        )
        self._sub_widgets.append(self._setting_gentexture_speed_text)
        self._setting_list.append(self._setting_gentexture_speed_text)

        self._setting_gentexture_speed_inputbox = MainScreen.setting_gentexture_speed_inputbox(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 6 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 1 // 13,
            ),
            text_hint=str(src.constants.SELECT_ATTEMPT),
        )
        self._sub_widgets.append(self._setting_gentexture_speed_inputbox)
        self._setting_list.append(self._setting_gentexture_speed_inputbox)

        self._setting_ai_ability_text = Text(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 7 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 1 // 13,
            ),
            text="AI智商:",
        )
        self._sub_widgets.append(self._setting_ai_ability_text)
        self._setting_list.append(self._setting_ai_ability_text)

        self._setting_ai_ability_inputbox = MainScreen.setting_ai_ability_inputbox(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 3 // 5,
                WINDOW_SIZE[1] * 8 // 13,
                WINDOW_SIZE[0] * 1.5 // 5,
                WINDOW_SIZE[1] * 1 // 13,
            ),
            text_hint=str(src.constants.AI_ABILITY),
        )
        self._sub_widgets.append(self._setting_ai_ability_inputbox)
        self._setting_list.append(self._setting_ai_ability_inputbox)

        self.visible = True

    class history_table(Table):
        def __init__(
            self,
            parent: Widget,
            rect: pygame.Rect,
            surface: pygame.Surface = None,
            present_number: int = 4,
        ) -> None:
            self._text_list = []
            super().__init__(
                parent, rect, surface, self._text_list, present_number
            )
            self.refresh()

        def refresh(self):
            self._boards = DATABASE.export()
            text_list = [
                [x.timestamp, x.competitor_black + " vs " + x.competitor_white]
                for x in self._boards
            ]
            if self._text_list != text_list:
                self.set_text_list(text_list)
                self._text_list = text_list

        def shift_in(self, duration: float):
            self._parent._board.load_board(Board())
            self._parent._board.editable = False
            self.refresh()
            return super().shift_in(duration)

        def draw_begin(self) -> None:
            if self.visible and len(self._boards) > 0:
                if (
                    self._parent._board._board
                    != self._boards[self._active_item]
                ):
                    self._parent._board.load_board(
                        self._boards[self._active_item]
                    )
            return super().draw_begin()

    class statistic_table(Table):
        def __init__(
            self,
            parent: Widget,
            rect: pygame.Rect,
            surface: pygame.Surface = None,
            present_number: int = 4,
        ) -> None:
            self._text_list = self.gen_textlist()
            super().__init__(
                parent, rect, surface, self._text_list, present_number
            )

        def gen_textlist(self):
            self._boards = [
                board for board in DATABASE.export() if board.winner != None
            ]
            count = defaultdict(int)
            for board in self._boards:
                if board.winner == 0:
                    count[board.competitor_black] += 1
                    count[board.competitor_white] -= 1
                else:
                    count[board.competitor_black] -= 1
                    count[board.competitor_white] += 1
            count = sorted(count.items(), key=lambda x: x[1], reverse=True)
            text_list = []
            for key, val in count:
                text_list.append(["Player: " + key, "Score: " + str(val)])
            return text_list

        def shift_in(self, duration: float):
            textlist = self.gen_textlist()
            if self._text_list != textlist:
                self.set_text_list(textlist)
                self._text_list = textlist
            return super().shift_in(duration)

    class setting_board_size_inputbox(InputBox):
        def activate_out(self, duration: float):
            super().activate_out(duration)
            try:
                tmp = eval(self.text)
                if (
                    type(tmp) == tuple
                    and len(tmp) == 2
                    and type(tmp[0]) == int
                    and type(tmp[1]) == int
                ):
                    src.constants.DEFAULT_BOARD_SIZE = tmp
                    self._parent._board.load_board(Board())
                    self.text_hint = str(tmp)
            except:
                pass
            self.text = ""

    class setting_gentexture_speed_inputbox(InputBox):
        def activate_out(self, duration: float):
            super().activate_out(duration)
            try:
                tmp = eval(self.text)
                if type(tmp) == int and tmp > 0:
                    src.constants.SELECT_ATTEMPT = tmp
                    self.text_hint = str(tmp)
            except:
                pass
            self.text = ""

    class setting_ai_ability_inputbox(InputBox):
        def activate_out(self, duration: float):
            super().activate_out(duration)
            try:
                tmp = eval(self.text)
                if type(tmp) == int and tmp > 0:
                    src.constants.AI_ABILITY = tmp
                    self.text_hint = str(tmp)
            except:
                pass
            self.text = ""

    @Widget.visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self.shift_in()
            else:
                self.shift_out()

    def shift_in(self):
        assert self._visible == False

        for widget in self._main_list:
            try:
                widget.visible = True
            except:
                pass

        self._visible = True
        self._flags.append(
            mosaic_effect(
                self._surface, "ease_in", (min(WINDOW_SIZE) // 10, 1), 1
            )
        )

    def shift_out(self, event: pygame.event.Event = None):
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

    def draw_begin(self) -> None:
        src.constants.GAME_BACKGROUND.draw()
        if self._current_list != self._history_list and (
            self._board._board.winner != None
            or len(self._board._board.available_place) == 0
        ):
            self._board.load_board(Board())

    def draw_end(self) -> None:
        if not self.visible:
            self._surface.blit(
                surface_mosaic(self._surface, min(WINDOW_SIZE) // 10), (0, 0)
            )

