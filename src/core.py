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

File: src/core.py
Description: 
    The core code section, which contains the definition of the board and the 
    determination of winning and losing positions.
"""
from typing import List, Set, Tuple
import numpy as np
import time

import src.constants
from src.constants import TIME_FORMAT


class Board:
    """An abstract wrap of the state of a game.
    
    Attributes:
        timestamp: The time when the game start.
        board_size: Size to the board.
        current_side: The current side of the player.
        winner: The final winner.
        winpath: The critical pieces for the winner.
        board: The board of the game.
        kifu: The kifu of the game.
        available_place: The set of available place in board.
        competitor_black: The name of the black competitor.
        competitor_white: The name of the white competitor.
    
    Functions:
        place(column, row): 
            Attempt to place one piece to the given position.
        cancel():
            Try to cancel the previous place.
    """

    def __init__(
        self,
        board_size: Tuple[int, int] = None,
        competitor_black: str = "",
        competitor_white: str = "",
    ) -> None:
        """Initialization to the board.

        Args:
            board_size (Tuple[int, int], optional): 
                The size of the board. Defaults to DEFAULT_BOARD_SIZE.
            competitor_black (str, optional): 
                The name of the black competitor. Defaults to "".
            competitor_white (str, optional): 
                The name of thw white competitor. Defaults to "".
        """
        if board_size == None:
            board_size = src.constants.DEFAULT_BOARD_SIZE
        assert board_size[0] > 0 and board_size[1] > 0

        self.timestamp = time.strftime(TIME_FORMAT, time.localtime(time.time()))
        self._BOARD_SIZE = board_size
        self.competitor_black = competitor_black
        self.competitor_white = competitor_white
        self._current_side = False
        self._winner = None
        self._winpath = None
        self._board = np.full(self._BOARD_SIZE, -1)
        self._available_place = set()
        for i in range(self._BOARD_SIZE[0]):
            for j in range(self._BOARD_SIZE[1]):
                self._available_place.add((i, j))
        self._kifu = list()

    @property
    def board_size(self) -> Tuple[int, int]:
        """Size to the board

        Returns:
            Tuple[int,int]: Board size:
                (WIDTH, HEIGHT)
        """
        return self._BOARD_SIZE

    @property
    def current_side(self) -> bool:
        """Current player's side.

        Returns:
            bool: Current side: 
                False : the black side.
                True  : the white side.
        """
        return self._current_side

    @property
    def winner(self):
        """The final winner

        Returns:
            NoneType or bool: 
                False : the black side.
                True  : the white side.
                None  : the game is not over :)
        """
        return self._winner

    @property
    def winpath(self):
        """The critical pieces for the winner.

        Returns:
            List[Tuple[int,int]]: List of the position to the pieces.
        """
        return None if self._winpath == None else self._winpath.copy()

    @property
    def board(self):
        """The board of the game

        Returns:
            ndarray: 
                Array to the board of the game, access by the board[column,row].
                Possible values:
                    0  : the black piece.
                    1  : the white piece.
                    -1 : the blank space.
                Note that the column and row START FROM ZERO (Compared to the 
                reality)!
        """
        return self._board.copy()

    @property
    def kifu(self) -> List[Tuple[int, int]]:
        """The kifu of the game

        Returns:
            List[Tuple[int, int]]: 
                List to the kifu of the game, each tuple indicate the (column, 
                row) of one piece, taken in the order black-white-black.Note 
                that the column and row START FROM ZERO (Compared to the 
                reality)!
        """
        return self._kifu.copy()

    @property
    def available_place(self) -> Set[Tuple[int, int]]:
        """The set of available place in board.

        Returns:
            Set[Tuple[int,int]]: The set of available place in board.
        """
        return self._available_place.copy()

    def place(self, column, row) -> None:
        """Attempt to place one piece to the given position.

        Args:
            column (int): The column of the position, start from 0.
            row (int): The row of the position, start from 0.
        """
        assert (column, row) in self._available_place
        assert self._winner == None
        self._available_place.remove((column, row))
        self._kifu.append((column, row))
        self._board[column, row] = self._current_side

        # Check winner
        direction = [
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
        ]
        direction_cnt = [1] * 4
        direction_path = [[(column, row)] for i in range(4)]
        for i in range(8):
            dc, dr = direction[i]
            c, r = column + dc, row + dr
            while (
                c in range(self._BOARD_SIZE[0])
                and r in range(self._BOARD_SIZE[1])
                and self._board[c, r] == self._current_side
            ):
                direction_cnt[i % 4] += 1
                direction_path[i % 4].append((c, r))
                c += dc
                r += dr
            if direction_cnt[i % 4] >= 5:
                self._winner = self._current_side
                self._winpath = direction_path[i % 4]

        self._current_side = not self._current_side

    def cancel(self) -> None:
        """Attempt to cancel the previous place.
        """
        assert len(self._kifu) > 0
        assert (
            self._kifu[-1][0],
            self._kifu[-1][1],
        ) not in self._available_place
        self._winner = None
        self._winpath = None
        self._available_place.add((self._kifu[-1][0], self._kifu[-1][1]))
        self._board[self._kifu[-1][0], self._kifu[-1][1]] = -1
        self._current_side = not self._current_side
        self._kifu.pop()
