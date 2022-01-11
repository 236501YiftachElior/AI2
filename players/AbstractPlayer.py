"""Abstract class of player. 
Your players classes must inherit from this.
"""
import utils
import numpy as np
from utils import get_directions
from SearchAlgos import State
class AbstractPlayer:
    """Your player must inherit from this class.
    Your player class name must be 'Player', as in the given examples (SimplePlayer, LivePlayer).
    Use like this:
    from players.AbstractPlayer import AbstractPlayer
    class Player(AbstractPlayer):
    """
    def __init__(self, game_time):
        """
        Player initialization.
        """
        self.game_time = game_time
        self.board = np.array(24)
        self.directions = utils.get_directions

    def set_game_params(self, board):
        """Set the game parameters needed for this player.
        This function is called before the game starts.
        (See GameWrapper.py for more info where it is called)
        input:
            - board: np.array of the board.
        No output is expected.
        """
        raise NotImplementedError

    def make_move(self, time_limit):
        """Make move with this Player.
        input:
            - time_limit: float, time limit for a single turn.
        output:
            - direction: tuple, specifing the Player's movement, (pos, soldier, dead_opponent_pos)
        """
        raise NotImplementedError

    def set_rival_move(self, move):
        """Update your info, given the new position of the rival.
        input:
            - pos: tuple, the new position of the rival.
        No output is expected
        """
        raise NotImplementedError

    def is_player(self, player, pos1, pos2, board=None):
        """
        Function to check if 2 positions have the player on them
        :param player: 1/2
        :param pos1: position
        :param pos2: position
        :return: boolean value
        """
        if board is None:
            board = self.board
        if board[pos1] == player and board[pos2] == player:
            return True
        else:
            return False

    def check_next_mill(self, position, player, board=None):
        """
        Function to check if a player can make a mill in the next move.
        :param position: curren position
        :param board: np.array
        :param player: 1/2
        :return:
        """
        if board is None:
            board = self.board
        mill = [
            (self.is_player(player, 1, 2, board) or self.is_player(player, 3, 5, board)),
            (self.is_player(player, 0, 2, board) or self.is_player(player, 9, 17, board)),
            (self.is_player(player, 0, 1, board) or self.is_player(player, 4, 7, board)),
            (self.is_player(player, 0, 5, board) or self.is_player(player, 11, 19, board)),
            (self.is_player(player, 2, 7, board) or self.is_player(player, 12, 20, board)),
            (self.is_player(player, 0, 3, board) or self.is_player(player, 6, 7, board)),
            (self.is_player(player, 5, 7, board) or self.is_player(player, 14, 22, board)),
            (self.is_player(player, 2, 4, board) or self.is_player(player, 5, 6, board)),
            (self.is_player(player, 9, 10, board) or self.is_player(player, 11, 13, board)),
            (self.is_player(player, 8, 10, board) or self.is_player(player, 1, 17, board)),
            (self.is_player(player, 8, 9, board) or self.is_player(player, 12, 15, board)),
            (self.is_player(player, 3, 19, board) or self.is_player(player, 8, 13, board)),
            (self.is_player(player, 20, 4, board) or self.is_player(player, 10, 15, board)),
            (self.is_player(player, 8, 11, board) or self.is_player(player, 14, 15, board)),
            (self.is_player(player, 13, 15, board) or self.is_player(player, 6, 22, board)),
            (self.is_player(player, 13, 14, board) or self.is_player(player, 10, 12, board)),
            (self.is_player(player, 17, 18, board) or self.is_player(player, 19, 21, board)),
            (self.is_player(player, 1, 9, board) or self.is_player(player, 16, 18, board)),
            (self.is_player(player, 16, 17, board) or self.is_player(player, 20, 23, board)),
            (self.is_player(player, 16, 21, board) or self.is_player(player, 3, 11, board)),
            (self.is_player(player, 12, 4, board) or self.is_player(player, 18, 23, board)),
            (self.is_player(player, 16, 19, board) or self.is_player(player, 22, 23, board)),
            (self.is_player(player, 6, 14, board) or self.is_player(player, 21, 23, board)),
            (self.is_player(player, 18, 20, board) or self.is_player(player, 21, 22, board))
        ]

        return mill[position]

    def is_mill(self, position, board=None):
        if board is None:
            board = self.board
        """
        Return True if a player has a mill on the given position
        :param position: 0-23
        :return:
        """
        if position < 0 or position > 23:
            return False
        p = int(board[position])

        # The player on that position
        if p != 0:
            # If there is some player on that position
            return self.check_next_mill(position, p, board)
        else:
            return False




def get_possible_mills():
    possible_mills = [
        [0, 1, 2],
        [0, 3, 5],
        [1, 9, 17],
        [2, 4, 7],
        [3, 11, 19],
        [4, 12, 20],
        [5, 6, 7],
        [6, 14, 22],
        [8, 9, 10],
        [8, 11, 13],
        [10, 12, 15],
        [13, 14, 15],
        [16, 17, 18],
        [16, 19, 21],
        [18, 20, 23],
        [21, 22, 23]

    ]
    return possible_mills


def get_possible_double_morris():
    double_mills = [
        [0, 1, 2, 4, 7],
        [0,1,2,3,5],
        [0,1,2,9,17],
        [2, 4, 7, 6, 5],
        [2, 4, 7, 12, 20],
        [7, 6, 5, 3, 0],
        [7,6,5,14,22],
        [8, 9, 10, 12, 15],
        [8, 9, 10, 11, 13],
        [8, 9, 10, 17, 1],
        [10, 12, 15, 14, 13],
        [10, 12, 15, 20, 4],
        [15, 14, 13, 11, 8],
        [15, 14, 13, 22, 6],
        [16, 17, 18, 20, 23],
        [16, 17, 18, 19, 21],

        [18, 20, 23, 22, 21],
        [23, 22, 21, 19, 16],
    ]
    return double_mills



def _get_possible_movements(self, position, board):
    directions = np.array(get_directions(position))
    return directions[np.argwhere(board[np.array(directions)] == 0)].squeeze(1)


def _heuristic(state: State, isMaximumPlayer):
    def mills_metric_count():
        possible_mills = get_possible_mills()
        scores = np.zeros((len(possible_mills), 3))
        total_score_almost = 0
        total_scores_closed = 0
        for mill_index, mill in enumerate(possible_mills):
            for placement in mill:
                if state.board_state[placement] >= 0:
                    scores[mill_index, int(state.board_state[placement])] = scores[
                                                                                mill_index, int(
                                                                                    state.board_state[placement])] + 1
            total_score_almost += 1 if scores[mill_index, 1] == 2 else -1 if scores[mill_index, 2] == 2 else 0
            total_scores_closed += 1 if scores[mill_index, 1] == 3 else -1 if scores[mill_index, 2] == 3 else 0
        return total_score_almost / len(possible_mills), total_scores_closed / len(possible_mills)

    def diff_blocked_pieces():
        my_blocked = 0
        rival_blocked = 0
        for rival_index in np.where(state.rival_pos >= 0)[0]:
            if len(get_possible_movements(state.rival_pos[rival_index], state.board_state)) == 0:
                rival_blocked += 1
        for my_index in np.where(state.my_pos >= 0)[0]:
            if len(get_possible_movements(state.my_pos[my_index], state.board_state)) == 0:
                my_blocked += 1
        return (rival_blocked - my_blocked) / (rival_blocked + my_blocked) if (rival_blocked + my_blocked) else 0

    def did_Close_Morris():
        return state.didCloseMorris if isMaximumPlayer else -state.didCloseMorris

    def double_morris():
        double_morris_options = get_possible_double_morris()
        player_1_double_morris = 0
        player_2_double_morris = 0
        for double_morris in double_morris_options:
            if state.board_state[double_morris[0]] == state.board_state[double_morris[1]] == \
                    state.board_state[double_morris[2]] == state.board_state[double_morris[3]] == \
                    state.board_state[double_morris[4]] != 0:
                player_1_double_morris = player_1_double_morris + 1 if state.board_state[double_morris[0]] == 1 \
                    else player_1_double_morris
                player_2_double_morris = player_2_double_morris + 1 if state.board_state[double_morris[0]] == 2 \
                    else player_2_double_morris
        double_morris_score = player_1_double_morris - player_2_double_morris

        return double_morris_score / 4

    def pieces_number():
        return (np.sum(state.my_pos >= 0) - np.sum(state.rival_pos >= 0)) / (np.sum(state.my_pos >= 0) + np.sum(state.rival_pos >= 0)) \
                if (np.sum(state.my_pos >= 0) + np.sum(state.rival_pos >= 0)) else 0

    almost_mills, closed_mills = mills_metric_count()
    if state.turn < 18:
        metric = ( 10 * pieces_number() + 10 * almost_mills + 10 * closed_mills + 7*double_morris()) / 38

    else:
        metric = (5 * diff_blocked_pieces() + 10 * pieces_number() + 10 * almost_mills + 10 * closed_mills + 5*double_morris()) / 41

    return metric


def get_possible_movements(position, board):
    directions = np.array(get_directions(position))
    return directions[np.argwhere(board[np.array(directions)] == 0)].squeeze(1)


def _is_player_blocked(state: State):
    pos = state.rival_pos if state.maximizingPlayer else state.my_pos
    for index_soldier, placement_soldier in enumerate(pos):
        if placement_soldier < 0:
            continue
        if len(get_possible_movements(placement_soldier, state.board_state)) > 0:
            return False
    return True


def _is_goal_state(state: State):
    if state.turn >= 18:
        if state.my_pos[state.my_pos != -2].size < 3 or state.rival_pos[state.rival_pos != -2].size < 3:
            # print("i made it")
            return True
        return _is_player_blocked(state)
    return False
