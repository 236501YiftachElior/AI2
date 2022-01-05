import operator
import numpy as np
import os

# TODO: edit the alpha and beta initialization values for AlphaBeta algorithm.
# instead of 'None', write the real initialization value, learned in class.
# hint: you can use np.inf
ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf


class State:
    def __init__(self, soldiers_p1, soldiers_p2, board_state, last_move, turn, maximizingPlayer, didCloseMorris):
        self.my_pos = soldiers_p1
        self.rival_pos = soldiers_p2
        self.board_state = board_state
        self.last_move = last_move
        self.turn = turn
        self.maximizingPlayer = maximizingPlayer
        self.didCloseMorris = didCloseMorris

    def copy(self):
        return State(self.my_pos.copy(), self.rival_pos.copy(), self.board_state.copy(), self.last_move, self.turn,
                     self.maximizingPlayer, self.didCloseMorris)


def get_directions(position):
    """Returns all the possible directions of a player in the game as a list.
    """
    assert 0 <= position <= 23, "illegal move"
    adjacent = [
        [1, 3],
        [0, 2, 9],
        [1, 4],
        [0, 5, 11],
        [2, 7, 12],
        [3, 6],
        [5, 7, 14],
        [4, 6],
        [9, 11],
        [1, 8, 10, 17],
        [9, 12],
        [3, 8, 13, 19],
        [4, 10, 15, 20],
        [11, 14],
        [6, 13, 15, 22],
        [12, 14],
        [17, 19],
        [9, 16, 18],
        [17, 20],
        [11, 16, 21],
        [12, 18, 23],
        [19, 22],
        [21, 23, 14],
        [20, 22]
    ]
    return adjacent[position]


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
        [2, 4, 7, 6, 5],
        [7, 6, 5, 3, 0],
        [5, 3, 0, 1, 2],
        [8, 9, 10, 12, 15],
        [10, 12, 15, 14, 13],
        [15, 14, 13, 11, 8],
        [13, 11, 8, 9, 10],
        [16, 17, 18, 20, 23],
        [18, 20, 23, 22, 21],
        [23, 22, 21, 19, 16],
        [21, 19, 16, 17, 18]

    ]
    return double_mills


def tup_add(t1, t2):
    """
    returns the sum of two tuples as tuple.
    """
    return tuple(map(operator.add, t1, t2))


def printBoard(board):
    print(int(board[0]), "(00)-----------------------", int(board[1]), "(01)-----------------------", int(board[2]),
          "(02)")
    print("|                             |                             |")
    print("|                             |                             |")
    print("|                             |                             |")
    print("|       ", int(board[8]), "(08)--------------", int(board[9]), "(09)--------------", int(board[10]),
          "(10)   |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       |        ", int(board[16]), "(16)-----", int(board[17]), "(17)-----", int(board[18]),
          "(18)   |        |")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print(int(board[3]), "(03)-", int(board[11]), "(11)---", int(board[19]), "(19)                 ",
          int(board[20]), "(20)-", int(board[12]), "(12)---", int(board[4]), "(04)")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print("|       |         |                       |        |        |")
    print("|       |        ", int(board[21]), "(21)-----", int(board[22]), "(22)-----", int(board[23]),
          "(23)   |        |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       |                     |                    |        |")
    print("|       ", int(board[13]), "(13)--------------", int(board[14]), "(14)--------------", int(board[15]),
          "(15)   |")
    print("|                             |                             |")
    print("|                             |                             |")
    print("|                             |                             |")
    print(int(board[5]), "(05)-----------------------", int(board[6]), "(06)-----------------------", int(board[7]),
          "(07)")
    print("\n")


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

    def blocked_opponent_pieces():
        metric = 0
        for rival_index in np.where(state.rival_pos >= 0)[0]:
            if len(get_possible_movements(state.rival_pos[rival_index], state.board_state)) == 0:
                metric += 1
        return metric / len(state.rival_pos)

    def diff_blocked_pieces():
        my_blocked = 0
        rival_blocked = 0
        for rival_index in np.where(state.rival_pos >= 0)[0]:
            if len(get_possible_movements(state.rival_pos[rival_index], state.board_state)) == 0:
                rival_blocked += 1
        for my_index in np.where(state.my_pos >= 0)[0]:
            if len(get_possible_movements(state.my_pos[my_index], state.board_state)) == 0:
                my_blocked += 1
        return (my_blocked - rival_blocked) / 18

    def did_Close_Morris():
        return state.didCloseMorris if isMaximumPlayer else -state.didCloseMorris

    def double_morris():
        double_morris_options = get_possible_double_morris()
        player_1_double_morris = 0
        player_2_double_morris = 0
        for double_morris in double_morris_options:
            if state.board_state[double_morris[0]] == state.board_state[double_morris[1]] == \
                    state.board_state[double_morris[2]] == state.board_state[double_morris[3]] == \
                    state.board_state[double_morris[4]]:
                player_1_double_morris = player_1_double_morris + 1 if state.board_state[double_morris[0]] == 1 \
                    else player_1_double_morris
                player_2_double_morris = player_2_double_morris + 1 if state.board_state[double_morris[0]] == 1 \
                    else player_2_double_morris
        double_morris_score = player_1_double_morris - player_2_double_morris
        return double_morris_score / 18

    def pieces_number():
        return (np.sum(state.my_pos >= 0) - np.sum(state.rival_pos >= 0)) / 18

    killing_score = np.sum(state.rival_pos == -2) / len(state.rival_pos) - np.sum(state.my_pos == -2) / len(
        state.my_pos)
    almost_mills, closed_mills = mills_metric_count()
    if state.turn < 18:
        metric = (
                         1 * did_Close_Morris() + 1 * killing_score + 1 * diff_blocked_pieces() + 1 * pieces_number() + 1 * almost_mills + 1 * closed_mills) / 7
        assert metric < 1, f"illegal metric size, too positive, was {metric}, " \
                           f"did_close_morris {did_Close_Morris()}, killing_score{killing_score}" \
                           f"diff_blocked_pieces{diff_blocked_pieces()},pieces_number{pieces_number()}, " \
                           f"almost_mills{almost_mills} closed_mills{closed_mills}"
    else:
        metric = (
                         1 * did_Close_Morris() + 1 * killing_score + 1 * diff_blocked_pieces() + 1 * pieces_number() + 1 * double_morris()) / 6
        assert metric < 1, f"illegal metric size, too positive, was {metric}, " \
                           f"did_close_morris {did_Close_Morris()}, killing_score{killing_score}" \
                           f"diff_blocked_pieces{diff_blocked_pieces()},pieces_number{pieces_number()}, " \
                           f"double_morris{double_morris()}"
    assert metric > -1, f"illegal metric size, too negative, was {metric}"
    # print(metric)
    return metric


def get_possible_movements(position, board):
    directions = np.array(get_directions(position))
    return directions[np.argwhere(board[np.array(directions)] == 0)].squeeze(1)


def _is_player_blocked(state: State):
    pos = state.my_pos if state.maximizingPlayer else state.rival_pos
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
