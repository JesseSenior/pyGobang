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

File: src/database.py
Description: 
    The database interaction part, which is responsible for storing as well as 
    reading the chess games.
"""
from typing import List
import sqlite3, pickle

from src.constants import (
    DEFAULT_DATABASE_PATH,
    DATABASE_CREATE_TABLE,
    DATABASE_INSERT_BOARD,
    DATABASE_SELECT_BOARD,
    DATABASE_DELETE_BOARD,
)
from src.core import Board


class BoardDatabase:
    """Database to save boards.
    
    Functions:
        append(board_to_save):
            Append the board to the database.
        export():
            Export the list of boards in the database.
        erase(board_timestamp):
            Erase the specified board, determined by its timestamp.
    """

    def __init__(self, database_path: str = DEFAULT_DATABASE_PATH) -> None:
        """Initialization to the board database.

        Args:
            database_path (str, optional): 
                The path to the database. If the file does not exist, it will
                create a new one. Defaults to DEFAULT_DATABASE_PATH.
        """
        self._conn = sqlite3.connect(database_path)
        self._cur = self._conn.cursor()
        self._cur.execute(DATABASE_CREATE_TABLE)

    def __del__(self):
        self._cur.close()
        self._conn.close()

    def append(self, board_to_save: Board) -> None:
        """Append the board to the database.

        Args:
            board_to_save (board): The specific board to save.
        """
        self._cur.execute(
            DATABASE_INSERT_BOARD,
            (
                board_to_save.timestamp,
                board_to_save.competitor_black,
                board_to_save.competitor_white,
                pickle.dumps(board_to_save.board_size),
                pickle.dumps(board_to_save.kifu),
                board_to_save.winner,
            ),
        )
        self._conn.commit()

    def export(self) -> List[Board]:
        """Export the list of boards in the database.

        Returns:
            List[board]: A list of the board stored in the database.
        """
        result = self._cur.execute(DATABASE_SELECT_BOARD)
        boards = list()
        for (
            timestamp,
            competitor_black,
            competitor_white,
            board_size,
            kifu,
            winner,
        ) in result:
            tmp = Board(
                pickle.loads(board_size), competitor_black, competitor_white
            )
            tmp.timestamp = timestamp
            for col, row in pickle.loads(kifu):
                tmp.place(col, row)
            assert tmp.winner == winner
            boards.append(tmp)
        return boards

    def erase(self, board_timestamp) -> None:
        """Erase the specified board, determined by its timestamp.

        Args:
            board_timestamp (str): The timestamp to the specified board.
        """
        self._cur.execute(DATABASE_DELETE_BOARD, (board_timestamp,))
        self._conn.commit()
