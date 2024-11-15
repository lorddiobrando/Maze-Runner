from Actor import *
from Maze import *

env=Maze(30,30,(25,25))

# env.Start('UCS',[[1 for i in range(32)] for j in range(61)])
# env.Start('BFS') 
# env.Start('greedy',HKey='Manhatten')
# env.Start('SA', HKey='Manhatten', SchedKey='Linear', Temp=1000)
# env.Start('DFS')
# env.Start('IDS')
env.Start('Astar', HKey='Manhatten', CostGrid=[[1 for i in range(31)] for j in range(31)])