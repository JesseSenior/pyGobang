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
from random import choice
import threading
from time import sleep
import pygame
import numpy as np
from pygame.constants import MOUSEBUTTONDOWN, BUTTON_LEFT
from math import ceil
from typing import List, Tuple
from src.display.effect import (
    alpha_effect,
    delayed_flag,
    surface_blur,
    temporary_flag,
)

from src.display.widget import Widget
from src.constants import (
    COLOR_BLACK,
    COLOR_BOARD,
    COLOR_RED,
    COLOR_TRANSPARENT,
    COLOR_WHITE,
)
from src.core import Board
from src.display.widget.background import Background
from src.players import Player, RobotPlayer


class UIPlayer(Player):
    def __init__(self, board_ui: BoardUI) -> None:
        super().__init__(board_ui._board)
        self._board_ui = board_ui


class MonkeyUIPlayer(UIPlayer):
    def __init__(self, board_ui: BoardUI) -> None:
        super().__init__(board_ui)
        self._thread = threading.Thread(target=self.place_a_piece)
        self._thread.start()

    def place_a_piece(self) -> None:
        sleep(0.5)
        self._board_ui.place_a_piece(choice(list(self.board.available_place)))


class HumanUIPlayer(UIPlayer):
    def __init__(self, board_ui: BoardUI) -> None:
        super().__init__(board_ui)
        self._col, self._row = self.board.board_size
        self._col_interval = board_ui._surface.get_size()[0] / (self._col + 1)
        self._row_interval = board_ui._surface.get_size()[1] / (self._row + 1)

        board_ui._handlers[MOUSEBUTTONDOWN].append(self._mouse_button_down)

    def _mouse_button_down(self, event: pygame.event.Event):
        if (
            pygame.Rect(
                *self._board_ui._surface.get_abs_offset(),
                *self._board_ui._surface.get_size()
            ).collidepoint(event.pos)
            and event.button == BUTTON_LEFT
        ):
            x = (
                event.pos[0]
                + self._col_interval / 2
                - self._board_ui._surface.get_abs_offset()[0]
            ) // self._col_interval
            y = (
                event.pos[1]
                + self._row_interval / 2
                - self._board_ui._surface.get_abs_offset()[1]
            ) // self._row_interval
            x, y = int(x), int(y)
            if 1 <= x <= self._col and 1 <= y <= self._row:
                self._board_ui.place_a_piece((x - 1, y - 1))
                pygame.mixer.Sound("res/sound/sound2.ogg").play()

    def stop_play(self) -> None:
        self._board_ui._handlers[MOUSEBUTTONDOWN].remove(
            self._mouse_button_down
        )


class RobotUIPlayer(UIPlayer, RobotPlayer):
    def __init__(self, board_ui: BoardUI) -> None:
        UIPlayer.__init__(self, board_ui)
        RobotPlayer.__init__(self, self.board)
        self._thread = threading.Thread(target=self.place_a_piece)
        self._thread.start()

    def place_a_piece(self) -> None:
        assert len(self.board.available_place) > 0
        if len(self.board.kifu) > 0:
            self.mcts.update_with_move(self.board.kifu[-1], False)
        move = self.mcts.get_move(self.board)
        self.mcts.update_with_move(move, False)
        self._board_ui.place_a_piece(move)
        pygame.mixer.Sound("res/sound/sound2.ogg").play()


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
            rect.size, "res/image/background2.png", COLOR_BOARD, False
        )
        self._surface_raw = pygame.Surface(self._surface.get_size())
        self._surface_raw.set_alpha(0)
        self._visible = False
        self._board_background.set_surface(
            self, self._surface_raw.get_rect(), self._surface_raw
        )
        self.load_board(board)
        self.set_player_list(player_list)

        self._last_sub_widgets = []
        self.editable = True

    def set_player_list(self, player_list: List[UIPlayer]):
        self._player_list = player_list
        self._current_player = (
            self._board.current_side
            if self._board.winner == None
            else self._board.winner
        )
        self._player = self._player_list[self._current_player](self)

    def load_board(self, board: Board):
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
        self._col_interval = self._surface.get_size()[0] / (self._col + 1)
        self._row_interval = self._surface.get_size()[1] / (self._row + 1)

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

            self._pre_flags.append(
                delayed_flag(
                    self._pre_flags,
                    lambda: temporary_flag(self, lambda: onexit()),
                    i * 0.08 + 0.5,
                )
            )

    def place_a_piece(self, pos: Tuple[int, int]):
        if self.editable:
            try:
                piece = BoardUI.Piece(
                    self,
                    self._surface.get_rect(),
                    self._surface_raw,
                    pos,
                    self._board,
                )
                self._sub_widgets.append(piece)
                self._current_player = (self._current_player + 1) % len(
                    self._player_list
                )
                self._player.stop_play()
                self._player = self._player_list[self._current_player](self)
            except:
                pass

    def cancel(self, step: int):
        if self.editable:
            try:
                for i in range(step):
                    self._board.cancel()
                    t = -1
                    while not self._sub_widgets[t].visible:
                        t -= 1
                    t = t + len(self._sub_widgets)
                    self._sub_widgets[t].visible = False
                    self._last_sub_widgets.append(self._sub_widgets[t])
                    self._sub_widgets.remove(self._sub_widgets[t])

                self._current_player = self._current_player - step
                while self._current_player < 0:
                    self._current_player += len(self._player_list)
                self._player.stop_play()
                self._player = self._player_list[self._current_player](self)
            except:
                pass

    def draw_begin(self) -> None:
        self._board_background.draw()
        self._surface_raw.blit(surface_blur(self._surface_raw, 3), (0, 0))
        self.draw_sub_widgets(self._last_sub_widgets)

    def draw_end(self) -> None:
        self._surface.blit(self._surface_raw, (0, 0))

    @Widget.visible.setter
    def visible(self, value: bool):
        if self._visible != value:
            if value:
                self.shift_in(1)
            else:
                self.shift_out(1)

    def shift_in(self, duration: float):
        assert self._visible == False

        def onexit():
            self._visible = True

        self._flags.append(
            alpha_effect(
                self._surface_raw, "ease_in", (0, 255), duration, onexit
            )
        )

    def shift_out(self, duration: float):
        assert self._visible == True

        self._visible = False

        self._flags.append(
            alpha_effect(self._surface_raw, "ease_out", (255, 0), duration)
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
            self._col_interval = self._surface.get_size()[0] / (self._col + 1)
            self._row_interval = self._surface.get_size()[1] / (self._row + 1)
            self._line_width = ceil(min(self._surface.get_size()) / 200)

        def draw_begin(self) -> None:
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
            self._col_interval = self._surface.get_size()[0] / (self._col + 1)
            self._row_interval = self._surface.get_size()[1] / (self._row + 1)
            self._pos = (
                pos[0] * self._col_interval,
                pos[1] * self._row_interval,
            )
            self._radius = min(self._surface.get_size()) / (self._col + 1) * 0.4
            self._surface_raw = pygame.Surface(
                self._surface.get_size()
            ).convert_alpha()
            self._surface_raw.fill(COLOR_TRANSPARENT)
            self._type = board.current_side if type == None else type
            if type == None:
                board.place(*self._pos_raw)
            self._surface_raw.set_alpha(0)
            self._visible = False
            self.visible = True

        def draw_begin(self) -> None:
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

        def draw_end(self) -> None:
            self._surface.blit(self._surface_raw, (0, 0))

        @Widget.visible.setter
        def visible(self, value: bool):
            if self._visible != value:
                if value:
                    self.shift_in(0.25)
                else:
                    self.shift_out(0.25)

        def shift_in(self, duration: float):
            assert self._visible == False

            self._visible = True

            self._flags.append(
                alpha_effect(self._surface_raw, "ease_in", (0, 255), duration)
            )

        def shift_out(self, duration: float):
            assert self._visible == True

            self._visible = False

            self._flags.append(
                alpha_effect(self._surface_raw, "ease_out", (255, 0), duration)
            )

