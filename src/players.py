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
    board. The partial code of MCTS is modified from the open source project 
    AlphaZero-Gomoku(https://github.com/junxiaosong/AlphaZero_Gomoku) licensed 
    under the MIT License. Thanks to their genius work!
"""
import numpy as np
from random import choice
from copy import deepcopy
from operator import itemgetter

import src.constants
import src.ai
from src.core import Board


class Player:
    """The general definition to the player.
    """

    def __init__(self, playing_board: Board) -> None:
        self.board = playing_board

    def place_a_piece(self) -> None:
        pass

    def stop_play(self) -> None:
        pass


class MonkeyPlayer(Player):
    """🐵: A cute monkey player, you will like it :)
    """

    def place_a_piece(self) -> None:
        self.board.place(*choice(list(self.board.available_place)))


class RobotPlayer(Player):
    """🤖: A cute robot player. Smarter than monkey :)
    
    Copyright statement: 
        The partial code of MCTS is modified from the open source project 
        AlphaZero-Gomoku(https://github.com/junxiaosong/AlphaZero_Gomoku) 
        licensed under the MIT License. Thanks to their genius work!
    """

    def place_a_piece(self) -> None:
        assert len(self.board.available_place) > 0

        move = src.ai.get_move(self.board)
        self.board.place(*move)


class HumanPlayer(Player):
    """😉: A cute human player. Smarter than robot, probably :)
    """

    def place_a_piece(self) -> None:
        c, r = map(int, input("Choose your column, row:").split())
        self.board.place(c, r)
