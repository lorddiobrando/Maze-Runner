from Actor import *
from Maze import *

env=Maze(10,10,(5,5))

# env.Start('UCS',[[1 for i in range(31)] for j in range(31)])
# env.Start('BFS')
# env.Start('greedy',HKey='Manhatten')
# env.Start('SA', HKey='Manhatten', SchedKey='Linear', Temp=10000)
# env.Start('DFS',[[1 for i in range(31)]]*31)
env.Start('IDS')