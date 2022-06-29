from avalon import *
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Run model of Avalon game.")
  parser.add_argument("-n", "--num_games", type=int, default=100, help="Number of simulated games that will be played to average the results.")
  parser.add_argument("-mer", "--merlin", type=bool, default=False, help="Specify whether to use a simplified version of Merlin as one of the good agents or not.")
  parser.add_argument("-hoe", "--higher_order_evil", type=bool, default=True, help="Specify whether evil agents use higher order knowledge or not.")
  parser.add_argument("-eaa", "--evil_agents_assasinate", type=bool, default=False, help="Specify whether evil agents can try to assasinate at the end of the game and win, this is done with a 1/3 chance.")
  args = parser.parse_args()

  num_games = args.num_games
  merlin = args.merlin
  higher_order_evil = args.higher_order_evil
  evil_agents_assasinate =  args.evil_agents_assasinate

  num_games = 100
  merlin = False
  higher_order_evil = True
  evil_agents_assasinate =  False

  # print(merlin)
  # print(higher_order_evil)
  # print(evil_agents_assasinate)

  num_good_wins = 0
  num_evil_wins = 0
  round_lengths = []
  for idx in range(num_games):
    good_won, evil_won, round_length = run_game(merlin, higher_order_evil, evil_agents_assasinate)
    round_lengths.append(round_length)
    if good_won:
      num_good_wins += 1
    elif evil_won:
      num_evil_wins += 1

print("Good winrate = " + str(num_good_wins / num_games))
print("Evil winrate = " + str(num_evil_wins / num_games))
print(round_lengths)