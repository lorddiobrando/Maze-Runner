from Actor import *
from Maze import *

width = 35
height=35 
goal = (random.randint(1, height-1), random.randint(1, width-1))
env=Maze(height,width,goal)
rand_cost = list(np.random.randint(1, 100, (height+1, width+1)))

#env.Start('Greedy',HKey='Manhatten')
env.Start('AStar',CostGrid=rand_cost,HKey='Manhatten')
#env.Start('DFS')
# env.Start('IDS')height = 35
# env.Start('GA', 20, 10000)
#env.Start('UCS', CostGrid=rand_cost)
# env.Start('BFS')
