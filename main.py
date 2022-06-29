from avalon import *
import argparse
import statistics

# helper function for argparser
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
  # parse command line arguments to chance settings of model
  parser = argparse.ArgumentParser(description="Run model of Avalon game.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-n", "--num_games", type=int, default=1000, help="Number of simulated games that will be played to average the results.")
  parser.add_argument("-mer", "--merlin", type=str2bool, nargs='?', const=True, default=False, help="Specify whether to use a simplified version of Merlin as one of the good agents or not.")
  parser.add_argument("-hoe", "--higher_order_evil", type=str2bool, nargs='?', const=True, default=False, help="Specify whether evil agents use higher order knowledge or not.")
  parser.add_argument("-eaa", "--evil_agents_assasinate", type=str2bool, nargs='?', const=True, default=False, help="Specify whether evil agents can try to assasinate at the end of the game and win, this is done with a 1/3 chance.")
  args = parser.parse_args()

  num_games = args.num_games
  merlin = args.merlin
  higher_order_evil = args.higher_order_evil
  evil_agents_assasinate =  args.evil_agents_assasinate

  print(merlin)
  print(higher_order_evil)
  print(evil_agents_assasinate)

  num_good_wins = 0
  num_evil_wins = 0
  game_lengths = []
  game_lengths_good_win = []
  game_lengths_evil_win = []
  for idx in range(num_games):
    good_won, evil_won, game_length = run_game(merlin, higher_order_evil, evil_agents_assasinate)
    game_lengths.append(game_length)
    if good_won:
      num_good_wins += 1
      game_lengths_good_win.append(game_length)
    elif evil_won:
      num_evil_wins += 1
      game_lengths_evil_win.append(game_length)

  print(f"Good winrate: {(num_good_wins / num_games):.2f}")
  print(f"Evil winrate: {(num_evil_wins / num_games):.2f}")

  print(f"average number of rounds all games: {statistics.mean(game_lengths)}")
  print(f"average number of rounds in games where Good won: {statistics.mean(game_lengths_good_win):.2f}")
  print(f"average number of rounds in games where Evil won: {statistics.mean(game_lengths_evil_win):.2f}")
