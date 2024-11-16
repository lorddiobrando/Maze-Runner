from Actor import *
from Maze import *

env=Maze(50,50,(42,25))

# env.Start('UCS',[[1 for i in range(21)] for j in range(61)])
# env.Start('BFS') 
# env.Start('greedy',HKey='Manhatten')
env.Start('Greedy',HKey='Manhatten')
#env.Start('DFS')
# env.Start('IDS')