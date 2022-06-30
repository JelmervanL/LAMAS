# Logical Aspects of Multi-Agent Systems 2022: Modelling Avalon Using Epistemic Logic

## Group 01
- Imme Huitema
- Anne-Jan Mein
- Jelmer van Lune

## Avalon
For this project the board game Avalon is modelled. In this model AI players play against each other using epistemic logic to make decisions. The rules of the game can be found [here](https://www.ultraboardgames.com/avalon/game-rules.php). 

## Running the code

First of all, make sure Python 3 is installed. 

The model with default settings can be ran for 1000 times using:
```bash
python3 main.py 
```

Different command line arguments can be given to change the settings of the model and simulation.

To see the different options and their defaults values use:

```bash
python3 main.py --help
```

This gives:
```
usage: main.py [-h] [-n NUM_GAMES] [-mer [MERLIN]] [-hoe [HIGHER_ORDER_EVIL]] [-eaa [EVIL_AGENTS_ASSASINATE]]

Run model of Avalon game.

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_GAMES, --num_games NUM_GAMES
                        Number of simulated games that will be played to average the results. (default: 1000)
  -mer [MERLIN], --merlin [MERLIN]
                        Specify whether to use a simplified version of Merlin as one of the good agents or not.
                        (default: False)
  -hoe [HIGHER_ORDER_EVIL], --higher_order_evil [HIGHER_ORDER_EVIL]
                        Specify whether evil agents use higher order knowledge or not. (default: False)
  -eaa [EVIL_AGENTS_ASSASINATE], --evil_agents_assasinate [EVIL_AGENTS_ASSASINATE]
                        Specify whether evil agents can try to assasinate Merlin at the end of the game and win, this is done with a 1/3 chance. Only possible when Merlin is included in the game. (default: False)
```

An example would be:
```bash
python3 main.py -n 2000 -mer True -hoe True -eaa False
```

This runs a simulation of the game 2000 times, with the inclusion of a simplified Merlin and evil agents use higher order knowledge for their reasoning. At the end of each game the evil agents cannot try to assasinate Merlin to still win. 

## Output
The output of the code is the win rate of team Good and team Evil over the number of games ran. Besides this, the average number of rounds in the games are reported. Moreover, plots of these statistics are presented.




