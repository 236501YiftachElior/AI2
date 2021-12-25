"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
import numpy as np
from SearchAlgos import MiniMax
from utils import Stage1State, Stage2State, _is_goal_state


class Player(AbstractPlayer):
    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.board = None
        self.game_time = game_time
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.minimax_stage1 = MiniMax(_construct_minimax_player_utility(self._heuristic), self._get_succ_states_stage1,
                                      None,
                                      _is_goal_state)
        self.minimax_stage2 = MiniMax(_construct_minimax_player_utility(self._heuristic), self._get_succ_states_stage2,
                                      None,
                                      _is_goal_state)

        self.board = None  # and add two more fields to Player
        self.my_pos = None
        self.rival_pos = None
        self.turn = 0

    def _get_succ_states_stage1(self, state):
        my_soldiers_count = (self.my_pos > 0).sum()
        rival_soldiers_count = (self.rival_pos > 0).sum()
        return [Stage1State(my_soldiers_count, rival_soldiers_count, placement, None, self.board)
                for placement in self.board if placement is not 0]

    def _get_succ_states_stage2(self, state):
        my_soldiers_count = (self.my_pos > 0).sum()
        rival_soldiers_count = (self.rival_pos > 0).sum()
        return [Stage2State(my_soldiers_count, rival_soldiers_count, position, self.directions(position), self.board)
                for position in self.my_pos if position >0]


    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array, of the board.
        No output is expected.
        """
        # TODO: erase the following line and implement this function.
        self.board = board
        self.my_pos = np.full(9, -1)
        self.rival_pos = np.full(9, -1)
        self.turn = 0
        # raise NotImplementedError

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement
        """
        if self.turn < 18:
            move = self._stage_1_move()
            self.turn += 1
            return move

        else:
            move = self._stage_2_move()
            self.turn += 1
            return move

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - move: tuple, the new position of the rival.
        No output is expected
        """
        # TODO: erase the following line and implement this function.
        rival_pos, rival_soldier, my_dead_pos = move

        ## add minimax iteration

        if self.turn < 18:
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        else:
            rival_prev_pos = self.rival_pos[rival_soldier]
            self.board[rival_prev_pos] = 0
            self.board[rival_pos] = 2
            self.rival_pos[rival_soldier] = rival_pos
        if my_dead_pos != -1:
            self.board[my_dead_pos] = 0
            dead_soldier = int(np.where(self.my_pos == my_dead_pos)[0][0])
            self.my_pos[dead_soldier] = -2
        self.turn += 1

    def _heuristic(self, state: Stage1State):
        # todo: add actual heuristic

        return 1

    def _stage_1_move(self):
        pass

    def _stage_2_move(self):
        pass


def _construct_minimax_player_utility(heuristic):
    def _minimax_utility_func(state, goal, maximizing_player):
        if goal:
            return 1 if maximizing_player else -1
        else:
            return heuristic(state)

    return _minimax_utility_func

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
