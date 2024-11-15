from Actor import *
from Maze import *

env=Maze(30,30,(30, 30))

env.Start('DFS',[[1 for i in range(31)]]*31)
