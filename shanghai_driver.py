from mcts import mcts

from shanghai_simulator import *

game = Shanghai(3)

mcts = mcts(iterationLimit = 100)

while not game.isTerminal():
    print(game)
    while game.curplayer == 0 and not game.isTerminal():
        bestAction = mcts.search(initialState=game) # search for ai move
        print(bestAction)
        game = game.takeAction(bestAction)                 # make ai move
    
    while game.curplayer != 0 and not game.isTerminal():
        fringe = game.getPossibleActions()
        rand = random.randint(0,len(fringe)-1)
        game = game.takeAction(fringe[rand])

print(game)