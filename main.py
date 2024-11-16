import numpy as np
from Actor import *
from Maze import *

height = 35
width = 35 
goal = (random.randint(1, height-1), random.randint(1, width-1))
env=Maze(height,width,goal)
rand_cost = list(np.random.randint(1, 100, (height+1, width+1)))

# env.Start('GA', 20, 10000)
env.Start('UCS', CostGrid=rand_cost)
# env.Start('BFS')
# env.Start('greedy',HKey='Manhatten')
# env.Start('SA', HKey='Manhatten', SchedKey='Linear')
# env.Start('DFS')
# env.Start('IDS')
# env.Start('Astar', HKey='Manhatten', CostGrid=[[1 for i in range(31)] for j in range(31)])
# env.Start('HC')
