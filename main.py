from avalon import *

if __name__ == "__main__":
  num_games = 100
  merlin = True
  higher_order_evil = False
  evil_agents_assasinate = True
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