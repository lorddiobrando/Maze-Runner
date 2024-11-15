from Actor import *
from Maze import *

env=Maze(10,10,(9,5))

env.Start('SA', HKey='Manhatten', SchedKey='Linear', Temp=10000)