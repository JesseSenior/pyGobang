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

    @staticmethod
    def rollout_policy_fn(board: Board):
        action_probs = np.random.rand(len(board.available_place))
        return zip(board.available_place, action_probs)

    @staticmethod
    def policy_value_fn(board: Board):
        action_probs = np.ones(len(board.available_place)) / len(
            board.available_place
        )
        return zip(board.available_place, action_probs), 0

    @staticmethod
    class node:
        """Tree node to the MCT.
        Original author: Junxiao Song.
        Modifier: Jesse Senior
        """

        def __init__(self, parent, prior_p):
            self._parent = parent
            self._children = {}
            self._n_visits = 0
            self._Q = 0
            self._u = 0
            self._P = prior_p

        @property
        def is_leaf(self):
            return self._children == {}

        def select(self, c_puct):
            return max(
                self._children.items(),
                key=lambda act_node: act_node[1].get_value(c_puct),
            )

        def get_value(self, c_puct):
            self._u = (
                c_puct
                * self._P
                * np.sqrt(self._parent._n_visits)
                / (1 + self._n_visits)
            )
            return self._Q + self._u

        def expand(self, action_priors):
            for action, prob in action_priors:
                if action not in self._children:
                    self._children[action] = RobotPlayer.node(self, prob)

        def update(self, leaf_value):
            self._n_visits += 1
            self._Q += 1.0 * (leaf_value - self._Q) / self._n_visits

        def update_recursive(self, leaf_value):
            if self._parent:
                self._parent.update_recursive(-leaf_value)
            self.update(leaf_value)

    @staticmethod
    class MCTS(object):
        """Main implementation to MCTS.
        Original author: Junxiao Song
        Modifier: Jesse Senior
        """

        def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):

            self._root = RobotPlayer.node(None, 1.0)
            self._policy = policy_value_fn
            self._c_puct = c_puct
            self._n_playout = n_playout

        def _playout(self, state: Board):
            node = self._root
            while not node.is_leaf:
                action, node = node.select(self._c_puct)
                state.place(*action)

            action_probs, _ = self._policy(state)
            if state.winner == None:
                node.expand(action_probs)
            leaf_value = self._evaluate_rollout(state)
            node.update_recursive(-leaf_value)

        def _evaluate_rollout(self, state: Board, limit=1000):
            player = state.current_side
            for i in range(limit):
                if state.winner != None or len(state.available_place) == 0:
                    break
                action_probs = RobotPlayer.rollout_policy_fn(state)
                max_action = max(action_probs, key=itemgetter(1))[0]
                state.place(*max_action)
            if state.winner == None:
                return 0
            else:
                return 1 if state.winner == player else -1

        def get_move(self, state):
            for n in range(self._n_playout):
                state_copy = deepcopy(state)
                self._playout(state_copy)
            return max(
                self._root._children.items(),
                key=lambda act_node: act_node[1]._n_visits,
            )[0]

        def update_with_move(self, last_move):
            if last_move in self._root._children:
                self._root = self._root._children[last_move]
                self._root._parent = None
            else:
                self._root = RobotPlayer.node(None, 1.0)

    def __init__(self, playing_board: Board, n_playout=10000) -> None:
        super().__init__(playing_board)
        self.mcts = RobotPlayer.MCTS(
            RobotPlayer.policy_value_fn, n_playout=n_playout
        )

    def place_a_piece(self) -> None:
        assert len(self.board.available_place) > 0
        if len(self.board.kifu) > 0:
            self.mcts.update_with_move(self.board.kifu[-1])
        move = self.mcts.get_move(self.board)
        self.board.place(*move)
        self.mcts.update_with_move(move)


class HumanPlayer(Player):
    """😉: A cute human player. Smarter than robot, probably :)
    """

    def place_a_piece(self) -> None:
        c, r = map(int, input("Choose your column, row:").split())
        self.board.place(c, r)
