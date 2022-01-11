import argparse
from GameWrapper import GameWrapper
import os, sys
import utils
import numpy as np


def experiment(heavy_depth):
    # for depth in range(heavy_depth,heavy_depth+3):
    heavy_ab_player_type = 'players.GlobalTimeABPlayer'
    light_ab_player_type = 'players.LightABPlayer'
    __import__(heavy_ab_player_type)
    __import__(light_ab_player_type)
    light_ab_player = sys.modules[light_ab_player_type].Player(200,3)
    heavy_ab_player = sys.modules[heavy_ab_player_type].Player(200)
    print('Starting Game!')
    print(heavy_ab_player_type, 'VS', light_ab_player_type)

    game = GameWrapper(player_1=light_ab_player, player_2=heavy_ab_player, players_positions=[np.full(9, -1), np.full(9, -1)],
                       print_game_in_terminal=True, time_to_make_a_move= 200, game_time=200)
    # while (True):
    game.run_game()

if __name__ == "__main__":
    players_options = [x+'Player' for x in ['Live', 'Simple', 'Minimax', 'Alphabeta', 'GlobalTimeAB', 'LightAB',
                                            'HeavyAB', 'Compete']]

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-player1', default='MinimaxPlayer', type=str,
                        help='The type of the first player.',
                        choices=players_options)
    parser.add_argument('-player2', default='AlphabetaPlayer',  type=str,
                        help='The type of the second player.',
                        choices=players_options)
    parser.add_argument('-move_time', default=40, type=float,
                        help='Time (sec) for each turn.')
    parser.add_argument('-game_time', default=2000, type=float,
                        help='Global game time (sec) for each player.')
    parser.add_argument('-terminal_viz', action='store_true',
                        help='Show game in terminal only.')
    parser.add_argument('-depth',default=3,type=float)

    args = parser.parse_args()

    #experiment(3)
    #exit(0)
    # check validity of game and turn times
    # if args.game_time < args.move_time:
    #     raise Exception('Wrong time arguments.')

    # Players inherit from AbstractPlayer - this allows maximum flexibility and modularity
    player_1_type = 'players.' + args.player1
    player_2_type = 'players.' + args.player2
    game_time = args.game_time
    depth = args.depth
    __import__(player_1_type)
    __import__(player_2_type)
    player_1 = sys.modules[player_1_type].Player(game_time)
    player_2 = sys.modules[player_2_type].Player(game_time)

    # print game info to terminal
    print('Starting Game!')
    print(args.player1, 'VS', args.player2)
    print('Players have', args.move_time, 'seconds to make a single move.')
    print('Each player has', game_time, 'seconds to play in a game (global game time, sum of all moves).')

    # create game with the given args
    game = GameWrapper(player_1=player_1, player_2=player_2,players_positions=[np.full(9, -1),np.full(9, -1)],
                    print_game_in_terminal=True,
                    time_to_make_a_move=args.move_time, 
                    game_time=game_time)
    # start playing!
    while(True):
        game.run_game()

