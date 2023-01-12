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
from typing import List

import src.constants
from src.constants import (
    DATABASE,
    SCREEN_CHANGE,
    WINDOW_SIZE,
    MAINSCREEN_BOARD_SIZE,
    EFFECT_DURATION_MINI,
    EFFECT_DURATION_NORMAL,
)
from src.core import Board
from src.display.tool import play_sound
from src.display.effect import (
    mosaic_effect,
    surface_mosaic,
    delayed_flag,
    temporary_flag,
)
from src.display.screen import Screen
from src.display.widget import Widget
from src.display.widget.board import BoardUI, MonkeyUIPlayer
from src.display.widget.button import Button
from src.display.widget.input_box import InputBox
from src.display.widget.logo import LOGO
from src.display.widget.table import Table
from src.display.widget.text import Text

MAINMENU_ID = 0
HISTORYMENU_ID = 1
STATISTICMENU_ID = 2
SETTINGMENU_ID = 3


class MainScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
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
        self._sub_widgets.append(self._game_logo)

        self._board = BoardUI(
            self,
            pygame.Rect(
                WINDOW_SIZE[0] * 0.5 / 5,
                WINDOW_SIZE[1] * 1.75 / 5,
                min(WINDOW_SIZE) * 2.75 / 5,
                min(WINDOW_SIZE) * 2.75 / 5,
            ),
            board=Board(MAINSCREEN_BOARD_SIZE),
            player_list=[MonkeyUIPlayer, MonkeyUIPlayer],
        )
        self._sub_widgets.append(self._board)

        self._sub_menu: List[Widget]
        self._sub_menu = list()
        menu_rect = pygame.Rect(
            WINDOW_SIZE[0] * 3 / 5,
            WINDOW_SIZE[1] / 13,
            WINDOW_SIZE[0] * 1.5 / 5,
            WINDOW_SIZE[1] / 13 * 11,
        )

        self._sub_menu.append(MainMenu(self, menu_rect))
        self._sub_menu.append(HistoryMenu(self, menu_rect))
        self._sub_menu.append(StatisticMenu(self, menu_rect))
        self._sub_menu.append(SettingMenu(self, menu_rect))

        self.visible = True

        self._current_list = MAINMENU_ID
        self._sub_widgets.extend(self._sub_menu)
        self._sub_menu[self._current_list].visible = True

    def _shift_in(self):
        assert self._visible == False

        self._visible = True
        self._flags["before_end"].append(
            mosaic_effect(
                self._surface,
                "ease_in",
                (min(WINDOW_SIZE) // 10, 1),
                EFFECT_DURATION_MINI,
            )
        )
        super()._shift_in()

    def _shift_out(self, event: pygame.event.Event = None):
        assert self._visible == True

        if event.type == QUIT:
            self._stop_loop = 0
            return

        for widget in self._sub_widgets:
            try:
                widget.visible = False
            except:
                pass

        play_sound("sound/sound3.ogg")

        def onexit(event):
            self._visible = False
            self._stop_loop = event.screen

        self._flags["before_end"].append(
            mosaic_effect(
                self._surface,
                "ease_out",
                (1, min(WINDOW_SIZE) // 10),
                EFFECT_DURATION_NORMAL,
                on_exit=lambda: onexit(event),
            )
        )

    def _draw_begin(self) -> None:
        src.constants.GAME_BACKGROUND.draw()
        if self._current_list != HISTORYMENU_ID and (
            self._board.board.winner != None
            or len(self._board.board.available_place) == 0
        ):
            self._board.load_board()

    def _draw_end(self) -> None:
        if not self.visible:
            self._surface.blit(
                surface_mosaic(self._surface, min(WINDOW_SIZE) // 10), (0, 0)
            )

    def _switch_to(self, list_id: int) -> None:
        if list_id != self._current_list:
            self._sub_menu[self._current_list].visible = False
            self._current_list = list_id

            def tmpfunc():
                self._sub_menu[self._current_list].visible = True

            self._flags["before_end"].append(
                delayed_flag(
                    self._flags["before_end"],
                    lambda: temporary_flag(self, tmpfunc),
                    EFFECT_DURATION_NORMAL,
                ),
            )


class MainMenu(Widget):
    def __init__(self, parent: MainScreen, rect: pygame.Rect) -> None:
        super().__init__(parent, rect)
        self.parent: MainScreen
        self._visible = False

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (1 - 1) * 2,
                    rect.width,
                    rect.height / 11,
                ),
                text="开始游戏",
                on_press=lambda: pygame.event.post(
                    pygame.event.Event(SCREEN_CHANGE, screen=3)
                ),
            )
        )

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (2 - 1) * 2,
                    rect.width,
                    rect.height / 11,
                ),
                text="历史对战",
                on_press=lambda: self.parent._switch_to(HISTORYMENU_ID),
            )
        )

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (3 - 1) * 2,
                    rect.width,
                    rect.height / 11,
                ),
                text="统计信息",
                on_press=lambda: self.parent._switch_to(STATISTICMENU_ID),
            )
        )

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (4 - 1) * 2,
                    rect.width,
                    rect.height / 11,
                ),
                text="设置",
                on_press=lambda: self.parent._switch_to(SETTINGMENU_ID),
            )
        )

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (5 - 1) * 2,
                    rect.width,
                    rect.height / 11,
                ),
                text="关于",
                on_press=lambda: print("作者是Jesse Senior~"),
            )
        )

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (6 - 1) * 2,
                    rect.width,
                    rect.height / 11,
                ),
                text="退出",
                on_press=lambda: pygame.event.post(pygame.event.Event(QUIT)),
            )
        )


class HistoryMenu(Widget):
    def __init__(self, parent: MainScreen, rect: pygame.Rect) -> None:
        super().__init__(parent, rect)
        self._visible = False

        self._parent: MainScreen
        self._board = self._parent._board

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    0,
                    rect.width,
                    rect.height / 11,
                ),
                text="返回",
                on_press=lambda: self._parent._switch_to(MAINMENU_ID),
            )
        )

        self._history_table = HistoryMenu.history_table(
            self,
            pygame.Rect(
                0,
                rect.height / 11 * (2 - 1) * 2,
                rect.width,
                rect.height / 11 * 7,
            ),
            self._board,
            present_number=7,
        )
        self._sub_widgets.append(self._history_table)

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (6 - 1) * 2,
                    rect.width / 5 * 2,
                    rect.height / 11,
                ),
                text="恢复",
                on_press=self.restore,
            )
        )

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    rect.width / 5 * 3,
                    rect.height / 11 * (6 - 1) * 2,
                    rect.width / 5 * 2,
                    rect.height / 11,
                ),
                text="删除",
                on_press=self.delete,
            )
        )

    def restore(self):
        if len(self._history_table.boards) > 0:
            src.constants.LAST_BOARD = self._history_table.boards[
                self._history_table.active_item
            ]
            pygame.event.post(pygame.event.Event(SCREEN_CHANGE, screen=3))

    def delete(self):
        if len(self._history_table.boards) > 0:
            DATABASE.erase(
                self._history_table.boards[
                    self._history_table.active_item
                ].timestamp
            )
            self._board.load_board()
            self._history_table.refresh()

    class history_table(Table):
        def __init__(
            self,
            parent: Widget,
            rect: pygame.Rect,
            board: BoardUI,
            surface: pygame.Surface = None,
            present_number: int = 4,
        ) -> None:
            self._text_list = []
            super().__init__(
                parent, rect, surface, self._text_list, present_number
            )
            self._board = board

        @property
        def boards(self):
            return self._boards

        @property
        def active_item(self):
            return self._active_item

        def refresh(self):
            self._boards = DATABASE.export()
            text_list = [
                [x.timestamp, x.competitor_black + " vs " + x.competitor_white]
                for x in self._boards
            ]
            if self._text_list != text_list:
                self.set_text_list(text_list)
                self._text_list = text_list
            if (
                len(self._boards) > 0
                and self._board.board != self._boards[self._active_item]
            ):
                self._board.load_board(self._boards[self._active_item])

        def _shift_in(self):
            self._board.editable = False
            self.refresh()
            if len(self._boards) > 0:
                self._board.load_board(self._boards[self._active_item])
            return super()._shift_in()

        def _shift_out(self):
            self._board.editable = True
            self._board.load_board()
            return super()._shift_out()

        def _active_item_change(self):
            self._board.load_board(self._boards[self._active_item])


class StatisticMenu(Widget):
    def __init__(self, parent: MainScreen, rect: pygame.Rect) -> None:
        super().__init__(parent, rect)
        self._visible = False

        self._parent: MainScreen

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    0,
                    rect.width,
                    rect.height / 11,
                ),
                text="返回",
                on_press=lambda: self._parent._switch_to(MAINMENU_ID),
            )
        )

        self._sub_widgets.append(
            StatisticMenu.statistic_table(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * (2 - 1) * 2,
                    rect.width,
                    rect.height / 11 * 9,
                ),
                present_number=9,
            )
        )

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

        def _shift_in(self):
            textlist = self.gen_textlist()
            if self._text_list != textlist:
                self.set_text_list(textlist)
                self._text_list = textlist
            return super()._shift_in()


class SettingMenu(Widget):
    def __init__(self, parent: MainScreen, rect: pygame.Rect) -> None:
        super().__init__(parent, rect)
        self._visible = False

        self._sub_widgets.append(
            Button(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 0,
                    rect.width,
                    rect.height / 11,
                ),
                text="返回",
                on_press=lambda: self._parent._switch_to(MAINMENU_ID),
            )
        )

        self._sub_widgets.append(
            Text(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 1,
                    rect.width,
                    rect.height / 11,
                ),
                text="棋盘尺寸:",
            )
        )

        self._sub_widgets.append(
            SettingMenu.setting_board_size_inputbox(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 2,
                    rect.width,
                    rect.height / 11,
                ),
                text_hint=str(src.constants.DEFAULT_BOARD_SIZE),
            )
        )

        self._sub_widgets.append(
            Text(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 3,
                    rect.width,
                    rect.height / 11,
                ),
                text="纹理质量:",
            )
        )

        self._sub_widgets.append(
            SettingMenu.setting_gentexture_speed_inputbox(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 4,
                    rect.width,
                    rect.height / 11,
                ),
                text_hint=str(src.constants.SELECT_ATTEMPT),
            )
        )

        self._sub_widgets.append(
            Text(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 5,
                    rect.width,
                    rect.height / 11,
                ),
                text="游戏BGM大小:",
            )
        )

        self._sub_widgets.append(
            SettingMenu.setting_music_volume_inputbox(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 6,
                    rect.width,
                    rect.height / 11,
                ),
                text_hint=str("{:.0%}".format(pygame.mixer.music.get_volume())),
            )
        )

        self._sub_widgets.append(
            Text(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 7,
                    rect.width,
                    rect.height / 11,
                ),
                text="游戏音效大小:",
            )
        )

        self._sub_widgets.append(
            SettingMenu.setting_sound_volume_inputbox(
                self,
                pygame.Rect(
                    0,
                    rect.height / 11 * 8,
                    rect.width,
                    rect.height / 11,
                ),
                text_hint=str("{:.0%}".format(src.constants.SOUND_VOLUME)),
            )
        )

    @property
    def board(self):
        self.parent._board: BoardUI
        return self.parent._board

    class setting_board_size_inputbox(InputBox):
        def _activate_out(self):
            try:
                import re

                tmp = re.findall("[0-9]+", self.text)
                src.constants.DEFAULT_BOARD_SIZE = int(tmp[0]), int(tmp[1])
                self._parent.board: BoardUI
                self._parent.board.load_board()
                self.text_hint = str(src.constants.DEFAULT_BOARD_SIZE)
            except:
                pass
            self.text = ""
            super()._activate_out()

    class setting_gentexture_speed_inputbox(InputBox):
        def _activate_out(self):
            try:
                tmp = eval(self.text)
                if type(tmp) == int and tmp > 0:
                    src.constants.SELECT_ATTEMPT = tmp
                    self.text_hint = str(tmp)
            except:
                pass
            self.text = ""
            super()._activate_out()

    class setting_music_volume_inputbox(InputBox):
        def _activate_out(self):
            try:
                import re
                pygame.mixer.music.set_volume(float(re.findall(r"\d+(?:\.\d+)?", self.text)[0]) / 100)

                self.text_hint = str(
                    str("{:.0%}".format(pygame.mixer.music.get_volume()))
                )
            except:
                pass
            self.text = ""
            super()._activate_out()

    class setting_sound_volume_inputbox(InputBox):
        def _activate_out(self):
            try:
                import re
                src.constants.SOUND_VOLUME = float(re.findall(r"\d+(?:\.\d+)?", self.text)[0]) / 100
                if src.constants.SOUND_VOLUME>1.0:
                    src.constants.SOUND_VOLUME=1.0
                self.text_hint = str(
                    str("{:.0%}".format(src.constants.SOUND_VOLUME))
                )
            except:
                pass
            self.text = ""
            super()._activate_out()
