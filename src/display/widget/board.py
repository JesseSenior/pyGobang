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

File: src/display/widget/board.py
Description: The widget for displaying the board.
"""
from __future__ import annotations
import threading
from time import sleep
import pygame
import numpy as np
from pygame.constants import MOUSEBUTTONDOWN, BUTTON_LEFT
from math import ceil, floor
from typing import List, Tuple
from src.display.effect import (
    alpha_effect,
    delayed_flag,
    surface_blur,
    temporary_flag,
)

from src.display.widget import Widget
from src.display.tool import play_sound
from src.constants import (
    COLOR_BLACK,
    COLOR_BOARD,
    COLOR_RED,
    COLOR_TRANSPARENT,
    COLOR_WHITE,
    MUTE_SOUND,
    EFFECT_DURATION_TINY,
    EFFECT_DURATION_MINI,
    EFFECT_DURATION_NORMAL,
    TIMER_TICK,
    res_path,
)
from src.core import Board
from src.display.widget.background import Background
from src.players import MonkeyPlayer, Player, RobotPlayer


class UIPlayer(Player):
    def __init__(self, board_ui: BoardUI) -> None:
        super().__init__(board_ui._board)
        self._board_ui = board_ui

    def place_a_piece(self) -> None:
        self._thread = threading.Thread(target=self._place_a_piece)
        self._thread.start()

    def _place_a_piece(
        self, move: Tuple[int, int] = None, mute_sound: bool = MUTE_SOUND
    ) -> None:
        if move == None:
            move = self.get_move()
        self._board_ui.place_a_piece(move, mute_sound, self)


class MonkeyUIPlayer(UIPlayer, MonkeyPlayer):
    def __init__(self, board_ui: BoardUI) -> None:
        super().__init__(board_ui)

    def _timer_tick(self, event: pygame.event.Event):
        for handler in self._board_ui._handlers[TIMER_TICK]:
            if handler.__qualname__ == self._timer_tick.__qualname__:
                self._board_ui._handlers[TIMER_TICK].remove(handler)
        self._place_a_piece(mute_sound=True)

    def place_a_piece(self) -> None:
        self._board_ui._handlers[TIMER_TICK].append(self._timer_tick)


class HumanUIPlayer(UIPlayer):
    def __init__(self, board_ui: BoardUI) -> None:
        super().__init__(board_ui)
        self._col, self._row = self.board.board_size
        self._col_interval = board_ui.rect.width / (self._col + 1)
        self._row_interval = board_ui.rect.height / (self._row + 1)

    def place_a_piece(self) -> None:
        self._board_ui._handlers[MOUSEBUTTONDOWN].append(
            self._mouse_button_down
        )

    def _mouse_button_down(self, event: pygame.event.Event):
        if (
            self._board_ui.abs_rect.collidepoint(event.pos)
            and event.button == BUTTON_LEFT
        ):
            x = (
                event.pos[0] + self._col_interval / 2 - self._board_ui.rect.x
            ) // self._col_interval
            y = (
                event.pos[1] + self._row_interval / 2 - self._board_ui.rect.y
            ) // self._row_interval
            move = (int(x) - 1, int(y) - 1)
            if move in self._board_ui._board.available_place:
                super()._place_a_piece(move)

    def __del__(self) -> None:
        try:
            self._board_ui._handlers[MOUSEBUTTONDOWN].remove(
                self._mouse_button_down
            )
        except:
            pass


class RobotUIPlayer(UIPlayer, RobotPlayer):
    pass


class BoardUI(Widget):
    def __init__(
        self,
        parent: Widget,
        rect: pygame.Rect,
        surface: pygame.Surface = None,
        board: Board = None,
        player_list: List[UIPlayer] = [HumanUIPlayer, HumanUIPlayer],
    ) -> None:
        super().__init__(parent, rect, surface)
        self._board_background = Background(
            rect.size, res_path("image/background2.png"), COLOR_BOARD, False
        )
        self._surface_raw = pygame.Surface(self._surface.get_size())
        self._surface_raw.set_alpha(0)
        self._visible = False
        self.editable = True

        self._board_background.set_surface(
            self, self._surface_raw.get_rect(), self._surface_raw
        )

        self._sub_widgets: List[Widget]
        self._player: UIPlayer
        self.load_board(board, player_list)

        self._last_sub_widgets = []

    @property
    def board(self):
        return self._board

    def set_player_list(self, player_list: List[UIPlayer]):
        _editable = self.editable
        self.editable = False

        self._player_list = player_list
        if self._board.winner != None:
            self._current_player = self._board.winner
        else:
            self._current_player = self._board.current_side

        try:
            del self._player
        except:
            pass

        self.editable = _editable
        self._player = self._player_list[self._current_player](self)
        if self._board.winner == None:
            self._player.place_a_piece()

    def load_board(
        self, board: Board = None, player_list: List[UIPlayer] = None
    ):
        _editable = self.editable
        self.editable = False
        for widget in reversed(self._sub_widgets):
            try:
                widget.visible = False
            except:
                pass
        self._last_sub_widgets = self._sub_widgets[1:]
        self._sub_widgets = []

        if board == None:
            board = Board()
        self._board = board

        self._col, self._row = board.board_size
        self._col_interval = self._surface.get_width() / (self._col + 1)
        self._row_interval = self._surface.get_height() / (self._row + 1)

        self._grid = BoardUI.Grid(
            self, self._surface_raw.get_rect(), self._surface_raw, board
        )
        self._sub_widgets.append(self._grid)
        self._pre_flags = []

        tmp = 0
        for i in range(len(self._board.kifu)):

            def onexit():
                nonlocal tmp
                try:
                    self._sub_widgets.append(
                        BoardUI.Piece(
                            self,
                            self._surface.get_rect(),
                            self._surface_raw,
                            self._board.kifu[tmp],
                            self._board,
                            tmp % 2 == 1,
                        )
                    )
                    tmp = tmp + 1
                except:
                    pass

            self._flags["after_begin"].append(
                delayed_flag(
                    self._flags["after_begin"],
                    lambda: temporary_flag(self, lambda: onexit()),
                    i * EFFECT_DURATION_MINI + EFFECT_DURATION_TINY,
                )
            )
        if player_list == None:
            player_list = self._player_list

        self.editable = _editable
        self.set_player_list(player_list)

    def place_a_piece(
        self,
        pos: Tuple[int, int],
        mute_sound: bool = False,
        current_player: UIPlayer = None,
    ):
        if not self.editable:
            return
        if current_player != None:
            if current_player != self._player:
                return

        try:
            piece = BoardUI.Piece(
                self,
                self._surface.get_rect(),
                self._surface_raw,
                pos,
                self._board,
            )
        except:
            return

        if not mute_sound:
            play_sound("sound/sound2.ogg")
        self._sub_widgets.append(piece)

        try:
            del self._player
        except:
            pass
        if self._board.winner == None:
            self._current_player = self._board._current_side
            self._player = self._player_list[self._current_player](self)
            self._player.place_a_piece()

    def cancel(self, step: int):
        if not self.editable:
            return

        try:
            for i in range(step):
                self._board.cancel()
                t = -1
                while not self._sub_widgets[t].visible:
                    t -= 1
                self._sub_widgets[t].visible = False
                self._last_sub_widgets.append(self._sub_widgets[t])
                self._sub_widgets.remove(self._sub_widgets[t])
        except:
            return
        self._current_player = self._board._current_side

        try:
            del self._player
        except:
            pass
        self._player = self._player_list[self._current_player](self)
        self._player.place_a_piece()

    def _draw_begin(self) -> None:
        self._board_background.draw()
        self._surface_raw.blit(surface_blur(self._surface_raw, 3), (0, 0))
        self._draw_sub_widgets(self._last_sub_widgets)

    def _draw_end(self) -> None:
        self._surface.blit(self._surface_raw, (0, 0))

    def _shift_in(self):
        assert self._visible == False

        self._visible = True

        self._flags["before_end"].append(
            alpha_effect(
                self._surface_raw,
                "linear",
                (0, 255),
                EFFECT_DURATION_NORMAL,
            )
        )

    def _shift_out(self):
        assert self._visible == True

        def on_exit():
            self._visible = False

        self._flags["before_end"].append(
            alpha_effect(
                self._surface_raw,
                "linear",
                (255, 0),
                EFFECT_DURATION_NORMAL,
                on_exit,
            )
        )

    class Grid(Widget):
        def __init__(
            self,
            parent: Widget,
            rect: pygame.Rect,
            surface: pygame.Surface = None,
            board: Board = None,
        ) -> None:
            super().__init__(parent, rect, surface)
            self._col, self._row = board.board_size
            self._col_interval = self._rect.width / (self._col + 1)
            self._row_interval = self._rect.height / (self._row + 1)
            self._line_width = ceil(min(self._rect.size) / 200) // 2 * 2 + 1

        def _draw_begin(self) -> None:
            for col in np.linspace(
                self._col_interval, self._col_interval * self._col, self._col
            ):
                pygame.draw.line(
                    self._surface,
                    COLOR_BLACK,
                    (col, self._row_interval),
                    (col, self._row_interval * self._row),
                    self._line_width,
                )
            for row in np.linspace(
                self._row_interval, self._row_interval * self._row, self._row
            ):
                pygame.draw.line(
                    self._surface,
                    COLOR_BLACK,
                    (self._col_interval, row),
                    (self._col_interval * self._col, row),
                    self._line_width,
                )

    class Piece(Widget):
        def __init__(
            self,
            parent: Widget,
            rect: pygame.Rect,
            surface: pygame.Surface = None,
            pos: Tuple[int, int] = (0, 0),
            board: Board = None,
            type: bool = None,
        ) -> None:
            super().__init__(parent, rect, surface)
            self._board = board
            self._pos_raw = pos
            pos = (pos[0] + 1, pos[1] + 1)
            self._col, self._row = board.board_size
            self._col_interval = self._rect.width / (self._col + 1)
            self._row_interval = self._rect.height / (self._row + 1)
            self._pos = (
                pos[0] * self._col_interval,
                pos[1] * self._row_interval,
            )
            self._radius = min(self._rect.size) / (self._col + 1) * 0.4
            self._surface_raw = pygame.Surface(self._rect.size).convert_alpha()
            self._surface_raw.fill(COLOR_TRANSPARENT)
            self._type = board.current_side if type == None else type
            if type == None:
                board.place(*self._pos_raw)
            self._surface_raw.set_alpha(0)
            self._visible = False
            self.visible = True

        def _draw_begin(self) -> None:
            pygame.draw.circle(
                self._surface_raw,
                COLOR_WHITE if self._type else COLOR_BLACK,
                self._pos,
                self._radius,
            )
            if (
                self._board.winpath != None
                and self._pos_raw in self._board.winpath
            ):
                pygame.draw.circle(
                    self._surface_raw,
                    COLOR_RED,
                    self._pos,
                    self._radius,
                    ceil(self._radius / 5),
                )
            else:
                pygame.draw.circle(
                    self._surface_raw,
                    COLOR_WHITE if not self._type else COLOR_BLACK,
                    self._pos,
                    self._radius,
                    ceil(self._radius / 20),
                )

        def _draw_end(self) -> None:
            self._surface.blit(self._surface_raw, (0, 0))

        def _shift_in(self):
            assert self._visible == False

            self._visible = True

            self._flags["before_end"].append(
                alpha_effect(
                    self._surface_raw,
                    "linear",
                    (0, 255),
                    EFFECT_DURATION_MINI,
                )
            )

        def _shift_out(self):
            assert self._visible == True

            self._visible = False

            self._flags["before_end"].append(
                alpha_effect(
                    self._surface_raw,
                    "linear",
                    (255, 0),
                    EFFECT_DURATION_MINI,
                )
            )
