"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
import numpy as np
from SearchAlgos import MiniMax
from utils import Stage1State, Stage2State, _is_goal_state
import time


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

    def _kill_by_heuristic(self,rival_cells:np.ndarray, state, isMaximumPlayer):
        return rival_cells[0]

    def _choose_cell_to_kill(self,state,isMaximumPlayer):
        rival_cells = np.where(self.board == 2)[0]
        rival_cell_idx = np.argmax(self._kill_by_heuristic(np.where(self.board == 2)[0],state,isMaximumPlayer))

        return rival_cells[rival_cell_idx]

    def _make_mill_get_cell(self,state,isMaximumPlayer):
        rival_cell = self._choose_cell_to_kill(state,isMaximumPlayer)
        rival_idx = np.where(self.rival_pos == rival_cell)[0][0]
        if isMaximumPlayer:
            self.rival_pos[rival_idx] = -2
            self.board[rival_cell] = 0
        else:
            state.my_pos[rival_idx] = -2
            state.board[rival_cell] = 0
        return rival_cell

    def _get_succ_states_stage1(self, state=None, isMaximumPlayer=True):
        if state == None:
            my_pos_copy = self.my_pos.copy()
            rival_pos_copy = self.rival_pos.copy()
            copy_board = self.board.copy()

        else:
            my_pos_copy = state.my_pos.copy()
            rival_pos_copy = state.rival_pos.copy()
            copy_board = state.board.copy()

        for placement in self.board:
            if placement == 0:
                continue
            if isMaximumPlayer:
                my_soldier_that_moved = int(
                    np.random.choice(np.where(my_pos_copy == -1)[0], 1)[0])  # choose random soldier
                my_pos_copy[my_soldier_that_moved] = placement
                rival_cell = -1 if not self.is_mill(placement) else self._make_mill_get_cell(state,isMaximumPlayer)
            else:
                rival_soldier_that_moved = int(
                    np.random.choice(np.where(rival_pos_copy == -1)[0], 1)[0])  # choose random soldier
                rival_pos_copy[rival_soldier_that_moved] = placement
                my_cell =  -1 if not self.is_mill(placement) else self._make_mill_get_cell(state,isMaximumPlayer)

            copy_board[placement] = 1 if isMaximumPlayer else 2
            yield Stage1State(my_pos_copy, rival_pos_copy, placement, copy_board)

    def _get_succ_states_stage2(self, state, isMaximumPlayer):
        if isMaximumPlayer:
            my_pos_copy = state.my_pos.copy()
        else:
            rival_pos_copy = state.rival_pos.copy()

        return [Stage2State(my_soldiers_count, rival_soldiers_count, position, self.directions(position), self.board)
                for position in self.my_pos if position > 0]

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
            move = self._stage_1_move(time_limit)
            self.turn += 1
            return move
        else:
            move = self._stage_2_move(time_limit)
            self.turn += 1
            return move

    def _execute_strategy_till_time(self, minimax_stage_search, time_limit):
        depth = 1
        time_remaining = time_limit
        while True:
            start = time.time()
            _, position, soldier, rival_cell_killed = minimax_stage_search.search(None, depth, True)
            end = time.time()
            interval = end - start
            time_remaining = time_remaining - interval
            if time_remaining - 2 * interval < 0:
                break
            depth = depth + 1
        return position, soldier, rival_cell_killed

    # TODO: update this shit
    def _stage_1_move(self, time_limit):
        position, soldier, rival_cell_killed = self._execute_strategy_till_time(self.minimax_stage1, time_limit)
        self.my_pos[soldier] = position
        self.board[position] = 1
        return position, soldier, rival_cell_killed

    def _stage_2_move(self, time_limit):
        position, soldier, rival_cell_killed = self._execute_strategy_till_time(self.minimax_stage2, time_limit)
        self.my_pos[soldier] = position
        self.board[position] = 1
        return position, soldier, rival_cell_killed

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
