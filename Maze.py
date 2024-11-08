from Actor import Actor
from pyamaze import maze,COLOR
import sys
oo=sys.maxsize
UNVISITED=oo
VISITED=1

class Maze:

    def __init__(self,width,height,GoalState=None):
        self.theMaze=maze(width,height)
        self.theMaze._goal=GoalState
        self.Actor=Actor(self.theMaze)
        self.Fire=Actor(self.theMaze,(0,width),color=COLOR.red)
        self.Grid=[[UNVISITED]*width]*height
        self.Blocked=self.theMaze.maze_map

    def  InitializeActor(self,state):
        self.Actor.theGUI.position=state

    def  InitializeFire(self,state):
        self.Fire.theGUI.position=state
    
    def SetGoal(self,GoalState):self.theMaze._goal=GoalState

    def LessGo(self):
        if(not self.theMaze._goal):
            print("ERROR: Set your goal state first :)")
            exit()
        self.theMaze.CreateMaze(loopPercent=100)
        self.Actor.theGUI.footprints=True
        self.Fire.theGUI.footprints=True
        self.Fire.Transition()
        self.Actor.Transition()

        



        