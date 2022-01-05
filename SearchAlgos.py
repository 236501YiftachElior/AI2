"""Search Algos: MiniMax, AlphaBeta
"""
# TODO: you can import more modules, if needed
# TODO: update ALPHA_VALUE_INIT, BETA_VALUE_INIT in utils
import time
import numpy as np
from utils import State

ALPHA_VALUE_INIT = -np.inf
BETA_VALUE_INIT = np.inf  # !!!!!


class SearchAlgos:
    def __init__(self, utility, succ, perform_move=None, goal=None):
        """The constructor for all the search algos.
        You can code these functions as you like to, 
        and use them in MiniMax and AlphaBeta algos as learned in class
        :param utility: The utility function.
        :param succ: The succesor function.
        :param perform_move: The perform move function.
        :param goal: function that check if you are in a goal state.
        """
        self.utility = utility
        self.succ = succ
        self.perform_move = perform_move
        self.goal = goal

    def search(self, state, depth, maximizing_player):
        pass


class MiniMax(SearchAlgos):
    """
    def search_old(self, state: State, depth, maximizing_player):
        # TODO: erase the following line and implement this function.
        if depth == 0 or self.goal(state):
            # print(state.last_move)
            return self.utility(state, self.goal(state), maximizing_player), state.last_move
        successor_states = [successor_state for successor_state in self.succ(state, maximizing_player)]
        options = [self.search(successor_state, depth - 1, not maximizing_player) for successor_state in
                   successor_states]

        # print("my options" if maximizing_player else "rival options",options)
        utilities = np.array([utility for utility, _ in options])
        if maximizing_player:
            # print("my directions", len(directions), directions)
            return np.max(utilities), successor_states[np.argmax(utilities)].last_move
        # print("rival directions", len(directions), directions)
        return np.min(utilities), successor_states[np.argmin(utilities)].last_move
    """

    def _inner_search(self, state: State, depth, maximizing_player):
        if depth == 0 or self.goal(state):
            return self.utility(state, self.goal(state), maximizing_player)
        options = self.succ(state, maximizing_player)
        if maximizing_player:
            currMax = -np.inf
            for option in options:
                v = self._inner_search(option, depth - 1, not maximizing_player)
                currMax = max(v, currMax)
            return currMax
        else:
            currMin = np.inf
            for option in options:
                v = self._inner_search(option, depth - 1, not maximizing_player)
                currMin = min(v, currMin)
            return currMin

    def search(self, state, depth, maximizing_player):
        currMax = -np.inf
        # options = self.succ(state, True)
        # for level_one_state in options:
        #     if self.goal(level_one_state):
        #         return 1, level_one_state.last_move
        options = self.succ(state, True)
        best_move = ()
        for option in options:
            v = self._inner_search(option, depth - 1, False)
            if v > currMax:
                currMax = v
                best_move = option.last_move
        return currMax, best_move

class AlphaBeta(SearchAlgos):

    def _inner_search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        if depth == 0 or self.goal(state):
            return self.utility(state, self.goal(state), maximizing_player)
        current_choice = -np.inf if maximizing_player else np.inf
        for successor_state in self.succ(state, maximizing_player):
            if maximizing_player:
                utility = self._inner_search(successor_state, depth - 1, not maximizing_player, alpha, beta)
                current_choice = max(utility, current_choice)
                alpha = max(alpha, current_choice)
                if current_choice >= beta:
                    return np.inf

            else:
                utility = self._inner_search(successor_state, depth - 1, not maximizing_player, alpha, beta)
                current_choice = min(utility, current_choice)
                beta = min(beta, current_choice)
                if current_choice <= alpha:
                    return -np.inf
        return current_choice

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        currMax = -np.inf
        options = self.succ(state, True)
        level_one_states = self.succ(state, True)
        for level_one_state in level_one_states:
            if self.goal(level_one_state):
                return 1, level_one_state.last_move
        best_move = ()
        for option in options:
            v = self._inner_search(option, depth - 1, False)
            if v > currMax:
                currMax = v
                best_move = option.last_move
        return currMax, best_move


class AlphaBetaSelectiveDeepeningTimeLimited(SearchAlgos):

    def _inner_search(self, state, depth, maximizing_player,  alpha=ALPHA_VALUE_INIT,
                      beta=BETA_VALUE_INIT,delta=0.01, remaining_time=None,):
        """Start the AlphaBeta algorithm.
        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :param alpha: alpha value
        :param: beta: beta value
        :return: A tuple: (The min max algorithm value, The direction in case of max node or None in min mode)
        """
        # TODO: erase the following line and implement this function.
        if remaining_time is not None and remaining_time <= 0:
            return self.utility(state, self.goal(state), maximizing_player)
        if depth == 0 or self.goal(state):
            current_utility = self.utility(state, self.goal(state), maximizing_player)
            maximizing_player_successor = not maximizing_player
            current_choice = -np.inf if maximizing_player_successor else np.inf
            for successor_state in self.succ(state, maximizing_player):
                suc_util = self.utility(successor_state, self.goal(successor_state),
                                    not maximizing_player)
                if suc_util - current_utility > delta:
                    utility = self._inner_search(successor_state, depth, not maximizing_player, alpha, beta)
                    if not maximizing_player:
                        current_choice = max(utility, current_choice)
                        alpha = max(alpha, current_choice)
                        if current_choice >= beta:
                            return np.inf

                    else:
                        current_choice = min(utility, current_choice)
                        beta = min(beta, current_choice)
                        if current_choice <= alpha:
                            return -np.inf
            if current_choice == -np.inf or current_choice == np.inf:
                return current_utility
            else:
                return current_choice
        current_choice = -np.inf if maximizing_player else np.inf
        for successor_state in self.succ(state, maximizing_player):
            utility = self._inner_search(successor_state, depth - 1, not maximizing_player, alpha, beta)
            if maximizing_player:
                current_choice = max(utility, current_choice)
                alpha = max(alpha, current_choice)
                if current_choice >= beta:
                    return np.inf

            else:
                current_choice = min(utility, current_choice)
                beta = min(beta, current_choice)
                if current_choice <= alpha:
                    return -np.inf
        return current_choice

    def search(self, state, depth, maximizing_player, alpha=ALPHA_VALUE_INIT, beta=BETA_VALUE_INIT):
        currMax = -np.inf
        options = self.succ(state, True)
        best_move = ()
        for option in options:
            v = self._inner_search(option, depth - 1, False)
            if v > currMax:
                currMax = v
                best_move = option.last_move
        return currMax, best_move
