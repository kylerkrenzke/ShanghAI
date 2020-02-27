import random

from mcts import mcts
from simulator import *

game = Simulator(3)
mcts = mcts(iterationLimit = 200)

while(1):
    print(game)
    while game.curplayer == 0 and not game.isTerminal():
        print(game.getPossibleActions())
        bestAction = mcts.search(initialState = game)
        print(bestAction)
        game = game.takeAction(bestAction)
    while game.curplayer != 0 and not game.isTerminal():
        fringe = game.getPossibleActions()
        rand = random.randint(0, len(fringe)-1)
        game = game.takeAction(fringe[rand])
print(game)