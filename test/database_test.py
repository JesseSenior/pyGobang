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

File: test/database_test.py
Description: Unit test of database.py
"""
from random import randrange
from time import sleep

import src.constants
from src.core import Board
from src.database import BoardDatabase
from src.players import MonkeyPlayer
from test.core_test import plot_board, info_of_board


def make_board(
    board_size=src.constants.DEFAULT_BOARD_SIZE,
    player_a="",
    player_b="",
    amount_of_attempt=50,
):
    abd = Board(board_size, player_a, player_b)
    p = MonkeyPlayer(abd)
    for t in range(amount_of_attempt):
        p.place_a_piece()
    return abd


if __name__ == "__main__":
    print("Initializing the database...")
    bdb = BoardDatabase()
    print("Done")

    print("Generate 3 random board and insert to the database")
    for i in range(3):
        bdb.append(
            make_board(
                (randrange(15, 19), randrange(15, 19)), "yoshabi", "woshabi", 50
            )
        )
        sleep(1)
    print("Done")

    print("Display all board")
    for bd in bdb.export():
        plot_board(bd, show_id=False)
        info_of_board(bd)
    print("Done")

    print("Delete all board")
    for bd in bdb.export():
        bdb.erase(bd.timestamp)
    print("Done")
