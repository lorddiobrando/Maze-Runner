from Actor import *
from Maze import *

env=Maze(20,20,(15,20))

# env.Start('UCS',[[1 for i in range(21)] for j in range(61)])
# env.Start('BFS') 
# env.Start('greedy',HKey='Manhatten')
# env.Start('SA', HKey='Manhatten', SchedKey='Linear', Temp=10000)
env.Start('DFS')
# env.Start('IDS')