from Actor import *
from Maze import *

env=Maze(10,10,(9,5))

# env.Start('greedy',HKey='Manhatten')
env.Start('SA', HKey='Manhatten', SchedKey='Linear', Temp=10000)