"""pyGobang, a python based Gobang game.

Copyright (C) 2022 Xshellye modified by Jesse Senior

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.

File: src/ai.py
Description: 🤖AI part of pyGobang.
Copyright statement: 
    The partial code of Minmax algorithm is modified from a open source project 
    GoBang-python-homework (https://github.com/Xshellye/GoBang-python-homework) 
    Thanks to their genius work!
"""

from typing import Tuple

from src.core import Board

LEFT_RIGHT = 0
TOP_BOTTOM = 1
LEFTTOP_RIGHTBOTTOM = 2
RIGHTTOP_LEFTBOTTOM = 3


class BoardAI:
    def __init__(self, chessdata):
        self._chess_data = chessdata  # 1 for self, 0 for empty, -1 for opponent
        self._row = len(chessdata)
        self._col = len(chessdata[0])

    def get_grade(self, point, index):
        grade = 0
        for k in range(4):
            count1, count2, wall = self.count(point, index, k)
            tempGrade = 0
            if count1 >= 5:
                return 100000
            elif count1 == 4 and count2 >= 5:
                tempGrade = 1600
            elif count1 == 4 and count2 < 5:
                tempGrade = 20
            elif count1 == 3 and count2 >= 5:
                tempGrade = 400
            elif count1 == 3 and count2 < 5:
                tempGrade = 10

            elif count1 == 2 and count2 >= 5:
                tempGrade = 100
            elif count1 == 2 and count2 < 5:
                tempGrade = 4
            elif count1 == 1 and count2 >= 5:
                tempGrade = 10
            elif count1 == 1 and count2 < 5:
                tempGrade = 1

            if wall:
                grade += (tempGrade) * 0.3
            else:
                grade += tempGrade
        return grade

    def down_chess(self, index):
        MaxGrade = 0
        MaxPoint = None
        point = (0, 0)
        for i in range(self._row):
            for j in range(self._col):
                if self._chess_data[i][j] != 0:
                    continue
                point = (i, j)
                myGrade = self.get_grade(point, index)
                enemyGrade = self.get_grade(point, -index)
                if myGrade >= 100000:
                    myGrade = 199999
                if myGrade >= 1600:
                    myGrade += 1201
                if myGrade >= 400:
                    myGrade += 301
                if myGrade >= 100:
                    myGrade += 31
                grade = max(myGrade, enemyGrade)
                if grade > MaxGrade:
                    MaxGrade = grade
                    MaxPoint = point
        self._chess_data[MaxPoint[0]][MaxPoint[1]] = index
        return MaxPoint

    def count(self, point, index, direction):
        x, y = point
        wall = False
        fg = 0
        count1 = count2 = 1
        if direction == LEFT_RIGHT:
            for i in range(y - 1, -1, -1):
                if self._chess_data[x][i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if i - 1 > -1 and self._chess_data[x][i - 1] == -index:
                        wall = True
                elif self._chess_data[x][i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            for i in range(y + 1, self._col):
                if self._chess_data[x][i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        i + 1 < self._col
                        and self._chess_data[x][i + 1] == -index
                    ):
                        wall = True
                elif self._chess_data[x][i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        if direction == TOP_BOTTOM:
            for i in range(x - 1, -1, -1):
                if self._chess_data[i][y] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if i - 1 > -1 and self._chess_data[i - 1][y] == -index:
                        wall = True
                elif self._chess_data[i][y] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            for i in range(x + 1, self._row):
                if self._chess_data[i][y] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        i + 1 < self._row
                        and self._chess_data[i + 1][y] == -index
                    ):
                        wall = True
                elif self._chess_data[i][y] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        if direction == LEFTTOP_RIGHTBOTTOM:
            n = min(x, y)
            for i in range(1, n):
                if self._chess_data[x - i][y - i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x - i - 1 > -1
                        and y - i - 1 > -1
                        and self._chess_data[x - i - 1][y - i - 1] == -index
                    ):
                        wall = True
                elif self._chess_data[x - i][y - i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            n = self._row - max(x, y)
            for i in range(1, n):
                if self._chess_data[x + i][y + i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x + i + 1 < n
                        and y + i + 1 < n
                        and self._chess_data[x + i + 1][y + i + 1] == -index
                    ):
                        wall = True
                elif self._chess_data[x + i][y + i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        if direction == RIGHTTOP_LEFTBOTTOM:
            n = min(x, self._row - y)
            for i in range(1, n):
                if self._chess_data[x - i][y + i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x - i - 1 > -1
                        and y + i + 1 < n
                        and self._chess_data[x - i - 1][y + i + 1] == -index
                    ):
                        wall = True
                elif self._chess_data[x - i][y + i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            n = min(self._row - x, y)
            for i in range(1, n):
                if self._chess_data[x + i][y - i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x + i + 1 < n
                        and y - i - 1 > -1
                        and self._chess_data[x + i + 1][y - i - 1] == -index
                    ):
                        wall = True
                elif self._chess_data[x + i][y - i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        return count1, count2, wall


def get_move(board: Board) -> Tuple[int, int]:
    assert len(board.available_place) > 0
    board_map = {False: {-1: 0, 0: 1, 1: -1}, True: {-1: 0, 0: -1, 1: 1}}
    converted_board = [
        [
            board_map[board.current_side][board.board[i][j]]
            for j in range(len(board.board))
        ]
        for i in range(len(board.board))
    ]
    return BoardAI(converted_board).down_chess(-1)

