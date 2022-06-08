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

File: test/core_test.py
Description: Unit testing of core.py.
"""
from os import system
from time import time

from src.core import Board
from src.players import HumanPlayer, RobotPlayer


def plot_board(test_board, show_id=True):
    if show_id:
        print(
            "  ◁ ",
            *["{: >2d}".format(x) for x in range(test_board.board_size[0])],
            "▷",
            sep=""
        )
        print("△ ", end="")
    print("  " + "▁" * (test_board.board_size[0]) * 2 + "  ")
    tmp = 0
    for col in test_board.board.T:
        if show_id:
            print("{: >2d}".format(tmp), end="")
        tmp += 1
        print(" ▐", end="")
        for x in col:
            if x == -1:
                print("＋", end="")
            elif x == 0:
                print("○", end=" ")
            else:
                print("●", end=" ")
        print("▌ ")
    if show_id:
        print("▽ ", end="")
    print("  " + "▔" * (test_board.board_size[0]) * 2 + "  ")


def info_of_board(test_board: Board):
    print("Board INFO:")
    print("-" * 10)
    print("- timestamp:", test_board.timestamp)
    print("- competitor_black:", test_board.competitor_black)
    print("- competitor_white:", test_board.competitor_white)
    print("- board_size:", test_board.board_size)
    print("- current_side:", test_board.current_side)
    print("- winner:", test_board.winner)
    print("-" * 10)


if __name__ == "__main__":
    print("Initializing the board...")
    test_board = Board((9, 9), "a", "b")
    print("Done, the information of the board is:")
    info_of_board(test_board)
    system("pause")

    # Robot vs Player
    players = [RobotPlayer(test_board, n_playout=6000), HumanPlayer(test_board)]
    # Player vs Player
    # players = [HumanPlayer(test_board), HumanPlayer(test_board)]
    current_player = 0
    time_begin = time_end = time()
    while True:
        system("cls")
        print("Previous time cost:", time_end - time_begin)
        plot_board(test_board)
        print("Current side:", ["○", "●"][test_board.current_side])
        if (
            type(players[current_player]) == HumanPlayer
            and len(test_board.kifu) > 1
        ):
            if (
                input(
                    "Previous player(%s )'s choice: (%d,%d), regret?(y/n)"
                    % (
                        ["○", "●"][1 - test_board.current_side],
                        *test_board.kifu[-1],
                    )
                )
                == "y"
            ):
                test_board.cancel()
                test_board.cancel()
                continue
        time_begin = time()
        players[current_player].place_a_piece()
        time_end = time()
        system("cls")
        plot_board(test_board)
        if test_board.winner != None:
            print("GAME OVER, WINNER: ", ["○", "●"][test_board.winner])
            if input("Regret?(y/n)") == "y":
                test_board.cancel()
                test_board.cancel()
            else:
                break
        current_player = 1 - current_player
