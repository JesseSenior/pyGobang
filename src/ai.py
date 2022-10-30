"""pyGobang, a python based Gobang game.

Copyright (C) 2022 Xshellye

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
"""

from turtle import down
from typing import Tuple
import numpy as np
from random import choice
from copy import deepcopy
from operator import itemgetter

import src.constants
from src.core import Board


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


LEFT_RIGHT = 0
TOP_BOTTOM = 1
LEFTTOP_RIGHTBOTTOM = 2
RIGHTTOP_LEFTBOTTOM = 3


class Chess:
    def __init__(self, chessdata):
        self.chessData = chessdata  # 1表示自己 0表示空 -1表示对手
        self.Row = len(chessdata)
        self.Col = len(chessdata[0])

    def GetGrade(self, point, index):
        grade = 0
        for k in range(4):
            count1, count2, isWall = self.Count(point, index, k)
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

            if isWall:
                grade += (tempGrade) * 0.3
            else:
                grade += tempGrade
        return grade

    def DownChess(self, index):
        MaxGrade = 0
        MaxPoint = None
        point = Point(0, 0)
        for i in range(self.Row):
            for j in range(self.Col):
                if self.chessData[i][j] != 0:
                    continue
                point.x = i
                point.y = j
                myGrade = self.GetGrade(point, index)
                enemyGrade = self.GetGrade(point, -index)
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
                    MaxPoint = Point(point.x, point.y)
        self.chessData[MaxPoint.x][MaxPoint.y] = index
        return MaxPoint

    def Count(self, point, index, direction):
        x = point.x
        y = point.y
        isWall = False
        fg = 0
        count1 = count2 = 1
        if direction == LEFT_RIGHT:
            for i in range(y - 1, -1, -1):
                if self.chessData[x][i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if i - 1 > -1 and self.chessData[x][i - 1] == -index:
                        isWall = True
                elif self.chessData[x][i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            for i in range(y + 1, self.Col):
                if self.chessData[x][i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if i + 1 < self.Col and self.chessData[x][i + 1] == -index:
                        isWall = True
                elif self.chessData[x][i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        if direction == TOP_BOTTOM:
            for i in range(x - 1, -1, -1):
                if self.chessData[i][y] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if i - 1 > -1 and self.chessData[i - 1][y] == -index:
                        isWall = True
                elif self.chessData[i][y] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            for i in range(x + 1, self.Row):
                if self.chessData[i][y] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if i + 1 < self.Row and self.chessData[i + 1][y] == -index:
                        isWall = True
                elif self.chessData[i][y] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        if direction == LEFTTOP_RIGHTBOTTOM:
            n = min(x, y)
            for i in range(1, n):
                if self.chessData[x - i][y - i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x - i - 1 > -1
                        and y - i - 1 > -1
                        and self.chessData[x - i - 1][y - i - 1] == -index
                    ):
                        isWall = True
                elif self.chessData[x - i][y - i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            n = self.Row - max(x, y)
            for i in range(1, n):
                if self.chessData[x + i][y + i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x + i + 1 < n
                        and y + i + 1 < n
                        and self.chessData[x + i + 1][y + i + 1] == -index
                    ):
                        isWall = True
                elif self.chessData[x + i][y + i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        if direction == RIGHTTOP_LEFTBOTTOM:
            n = min(x, self.Row - y)
            for i in range(1, n):
                if self.chessData[x - i][y + i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x - i - 1 > -1
                        and y + i + 1 < n
                        and self.chessData[x - i - 1][y + i + 1] == -index
                    ):
                        isWall = True
                elif self.chessData[x - i][y + i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
            fg = 0
            n = min(self.Row - x, y)
            for i in range(1, n):
                if self.chessData[x + i][y - i] == index and fg == 0:
                    count1 += 1
                    count2 += 1
                    if (
                        x + i + 1 < n
                        and y - i - 1 > -1
                        and self.chessData[x + i + 1][y - i - 1] == -index
                    ):
                        isWall = True
                elif self.chessData[x + i][y - i] == 0:
                    count2 += 1
                    fg = 1
                else:
                    break
        return count1, count2, isWall

    def JudgeWin_Lose(self, point, index):
        for i in range(4):
            if self.Count(point, index, i)[0] >= 5:
                return True


def get_move(board: Board) -> Tuple[int, int]:
    currenctside = board.current_side
    tmpboard = board.board
    for i in range(len(tmpboard)):
        for j in range(len(tmpboard[0])):
            if tmpboard[i][j] == -1:
                tmpboard[i][j] = 0
            elif tmpboard[i][j] == 0 and currenctside == False:
                tmpboard[i][j] = 1
            elif tmpboard[i][j] == 0 and currenctside == True:
                tmpboard[i][j] = -1
            elif tmpboard[i][j] == 1 and currenctside == True:
                tmpboard[i][j] = 1
            elif tmpboard[i][j] == 1 and currenctside == False:
                tmpboard[i][j] = -1
    aibot = Chess(tmpboard)
    point = aibot.DownChess(-1)
    return (point.x, point.y)
