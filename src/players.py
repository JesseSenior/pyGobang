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

File: src/players.py
Description: 
    A collection of the players, which is the general way to interact with the 
    board. 
"""
from typing import Tuple
from random import choice

import src.constants
import src.ai
from src.core import Board


class Player:
    """General definition to the player."""

    def __init__(self, playing_board: Board) -> None:
        """Initialize the player with current playing board.

        Args:
            playing_board (Board): Current playing board.
        """
        self.board = playing_board

    def get_move(self) -> Tuple[int, int]:
        """Attempt to get player's move.

        Notice:
            This function should NOT place any pieces!

        Returns:
            Tuple[int, int]: Move of player.
        """
        pass

    def place_a_piece(self) -> None:
        self.board.place(*self.get_move())


class MonkeyPlayer(Player):
    """🐵: A cute monkey player, you will like it :)"""

    def get_move(self) -> Tuple[int, int]:
        if len(self.board.available_place) == 0:
            return (0, 0)
        return choice(list(self.board.available_place))


class RobotPlayer(Player):
    """🤖: A cute robot player. Smarter than monkey :)"""

    def get_move(self) -> Tuple[int, int]:
        return src.ai.get_move(self.board)


class HumanPlayer(Player):
    """😉: A cute human player. Smarter than robot, probably :)"""

    def get_move(self) -> Tuple[int, int]:
        move = tuple(map(int, input("Choose your column, row:").split()))
        assert move in self.board.available_place

        return move
