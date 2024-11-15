from Actor import *
from Maze import *

env=Maze(10,10,(5,9))

env.Start('greedy',HKey='Manhatten')