"""
MiniMax Player
"""
from players.AbstractPlayer import AbstractPlayer
# TODO: you can import more modules, if needed
import numpy as np
from SearchAlgos import MiniMax
from utils import _is_goal_state, State, get_possible_mills
import time


class Player(AbstractPlayer):
    branching_factor = 50

    def __init__(self, game_time):
        AbstractPlayer.__init__(self, game_time)  # keep the inheritance of the parent's (AbstractPlayer) __init__()
        self.board = None
        self.game_time = game_time
        # TODO: initialize more fields, if needed, and the AlphaBeta algorithm from SearchAlgos.py
        self.minimax = MiniMax(_construct_minimax_player_utility(self._heuristic), self.get_succ,
                               None,
                               _is_goal_state)

        self.board = None  # and add two more fields to Player
        self.my_pos = None
        self.rival_pos = None
        self.turn = 0

    def _get_succ_stage_1(self, state: State, isMaximumPlayer):
        for placement in np.where(state.board_state == 0)[0]:
            state_copy = state.copy()
            my_pos_copy = state_copy.my_pos
            rival_pos_copy = state_copy.rival_pos
            board_copy = state_copy.board_state
            if isMaximumPlayer:
                # print("my pos copy is:",my_pos_copy,"state turn is ",state.turn)

                board_copy[placement] = 1
                pos_index = np.argwhere(my_pos_copy == -1)[0][0]
                my_pos_copy[pos_index] = placement
                if self.is_mill(placement, board_copy):
                    for st in _get_states_from_mill(placement, pos_index, state_copy.turn, board_copy, my_pos_copy,
                                                    rival_pos_copy, isMaximumPlayer):
                        yield st
                else:
                    last_move = (placement, pos_index, -1)
                    yield State(my_pos_copy, rival_pos_copy, board_copy, last_move, state_copy.turn + 1)
            else:
                # print("rival pos copy is:",rival_pos_copy,"state turn is",state_copy.turn)
                board_copy[placement] = 2
                pos_index = np.argwhere(rival_pos_copy == -1)[0][0]
                rival_pos_copy[pos_index] = placement
                if self.is_mill(placement, board_copy):
                    for st in _get_states_from_mill(placement, pos_index, state_copy.turn, board_copy, my_pos_copy,
                                                    rival_pos_copy, isMaximumPlayer):
                        yield st
                else:
                    last_move = (placement, pos_index, -1)
                    yield State(my_pos_copy, rival_pos_copy, board_copy, last_move, state_copy.turn + 1)

    # TODO broken
    def _get_succ_stage_2(self, state: State, isMaximumPlayer):

        if isMaximumPlayer:
            for index_soldier, placement_soldier in enumerate(state.my_pos):
                state_copy = state.copy()
                my_pos_copy = state_copy.my_pos
                rival_pos_copy = state_copy.rival_pos
                board_copy = state_copy.board_state
                if placement_soldier == -2:
                    continue
                for direction in self._get_possible_movements(placement_soldier, board_copy):
                    board_copy[placement_soldier] = 0
                    my_pos_copy[index_soldier] = direction
                    board_copy[direction] = 1
                    if self.is_mill(direction, board_copy):
                        for st in _get_states_from_mill(direction, index_soldier, state_copy.turn, board_copy,
                                                        my_pos_copy,
                                                        rival_pos_copy, isMaximumPlayer):
                            yield st
                    else:
                        last_move = (direction, index_soldier, -1)
                        yield State(my_pos_copy, rival_pos_copy, board_copy, last_move, state_copy.turn + 1)
        else:
            for index_soldier, placement_soldier in enumerate(state.rival_pos):
                state_copy = state.copy()
                my_pos_copy = state_copy.my_pos
                rival_pos_copy = state_copy.rival_pos
                board_copy = state_copy.board_state
                if placement_soldier == -2:
                    continue
                for direction in self._get_possible_movements(placement_soldier, board_copy):
                    board_copy[placement_soldier] = 0
                    rival_pos_copy[index_soldier] = direction
                    board_copy[direction] = 2
                    if self.is_mill(direction, board_copy):
                        for st in _get_states_from_mill(direction, index_soldier, state_copy.turn, board_copy,
                                                        my_pos_copy,
                                                        rival_pos_copy, isMaximumPlayer):
                            yield st
                    else:
                        last_move = (direction, index_soldier, -1)
                        yield State(my_pos_copy, rival_pos_copy, board_copy, last_move, state_copy.turn + 1)

    def _get_possible_movements(self, position, board):
        directions = np.array(self.directions(position))
        return directions[np.argwhere(board[np.array(directions)] == 0)].squeeze(1)

    def get_succ(self, state, isMaximumPlayer=True):
        if state.turn < 18:
            return self._get_succ_stage_1(state, isMaximumPlayer)
        else:
            return self._get_succ_stage_2(state, isMaximumPlayer)

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
        depth = 1
        time_remaining = time_limit
        while True:
            start = time.time()
            start_state = State(self.my_pos, self.rival_pos, self.board, None, self.turn)
            _, (position, soldier, rival_cell_killed) = self.minimax.search(start_state, depth, True)
            end = time.time()
            interval = end - start
            time_remaining = time_remaining - interval
            if time_remaining - interval * self.branching_factor < 0:
                break
            depth = depth + 1
        if self.my_pos[soldier] != -1:
            self.board[self.my_pos[soldier]] = 0
        self.my_pos[soldier] = position
        self.board[position] = 1
        self.turn += 1
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

    def _heuristic(self, state: State):
        possible_mills = get_possible_mills()
        scores = np.zeros((len(possible_mills), 3))
        total_score = 0
        for mill_index, mill in enumerate(possible_mills):
            for placement in mill:
                if state.board_state[placement] >= 0:
                    scores[mill_index, int(state.board_state[placement])] = scores[
                                                                           mill_index, int(state.board_state[placement])] + 1
            total_score += 1 if scores[mill_index, 1] == 2 else -1 if scores[mill_index, 2] == 2 else 0
        return total_score / len(possible_mills)


def _construct_minimax_player_utility(heuristic):
    def _minimax_utility_func(state, goal, maximizing_player):
        if goal:
            return 1 if maximizing_player else -1
        else:
            return heuristic(state)

    return _minimax_utility_func


def _get_states_from_mill(last_placement, soldier_to_place, turn, board, my_pos_copy,
                          rival_pos_copy, isMaximumPlayer):
    if isMaximumPlayer:
        attacked_soldiers = rival_pos_copy
    else:
        attacked_soldiers = my_pos_copy
    for index_player_to_remove, placement_player_to_remove in enumerate(attacked_soldiers):
        if placement_player_to_remove == -1:
            continue
        attacked_soldiers[index_player_to_remove] = -2
        board[placement_player_to_remove] = 0
        last_move = (last_placement, soldier_to_place, placement_player_to_remove)
        yield State(my_pos_copy, rival_pos_copy, board, last_move, turn + 1)


def _get_info_from_mill(attacked_soldiers):
    for index_soldier_to_remove, placement_soldier_to_remove in enumerate(attacked_soldiers):
        if placement_soldier_to_remove == -1:
            continue
        yield index_soldier_to_remove, placement_soldier_to_remove

    ########## helper functions in class ##########
    # TODO: add here helper functions in class, if needed

    ########## helper functions for AlphaBeta algorithm ##########
    # TODO: add here the utility, succ, an
