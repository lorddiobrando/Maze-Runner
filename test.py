from pyamaze import *
mz=maze(5,5)
mz._goal=(4,4)
mz.CreateMaze(loopPercent=100) # creating the maze
a=agent(mz,2,3,footprints=True) # creating an agent with its initial location, and whether to leave a footprint or not
f=agent(mz,1,1,footprints=True,shape='arrow',)
a.position=(3,4) #Moves the agent to specified position
a.position=(2,4)
print(mz.maze_map) # Maze map is responsible for determining whether a certain position is able to move east, west, north, or south
mz.run()

