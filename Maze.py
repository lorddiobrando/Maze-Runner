from Actor import * 
from pyamaze import maze,COLOR
from collections import deque
from heapq import heappop,heappush
import sys
oo=sys.maxsize
UNVISITED=oo
VISITED=1
FIRE=-oo
X=0
Y=1

class Maze:

    def __init__(self,width,height,GoalState=None,ActorState=(1,1)):
        self.theMaze=maze(width,height)
        self.theMaze.CreateMaze(loopPercent=50)
        self.Agent=Actor(self.theMaze,ActorState)
        if GoalState==None:self.Goal=(width,height)
        else: self.Goal=GoalState

        self.Grid=[[UNVISITED for i in range(width+1)] for j in range(height+1)]
        self.Functions={
            'UCS':self.UCS
        }

    def SearchFunction(self,Key,Cost=None):
        self.Functions[Key.upper()](Cost)

    def Start(self,Key,CostGrid):
        if(not self.Goal or not self.Agent.State):
            print("ERROR: Set all your States first :)")
            exit()
        self.Agent.theGUI.footprints=True
        self.SearchFunction(Key,CostGrid)
        self.theMaze.run()

#--------------------------------------------------------------------------
# Enter your Search Algorithms here

    def UCS(self,CostGrid=None):
        Queue=[(0,self.Agent.State)]
        print("Begin")
        if(not CostGrid):
            print("ERROR: Chose UCS Search with no Cost Inserted :)")
            exit()
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]]=0
        while Queue:
            CurrCost,CurrState=heappop(Queue)
            if CurrCost>self.Grid[CurrState[X]][CurrState[Y]] or CurrCost==FIRE: continue
            self.Agent.NowState(CurrState)
            self.Agent.draw()
            for state in self.Agent.Actions():
                if CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]>=self.Grid[state[X]][state[Y]]: continue
                self.Grid[state[X]][state[Y]]=CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]
                heappush(Queue,(self.Grid[state[X]][state[Y]],state))
        if(self.Grid[self.Goal[X]][self.Goal[Y]]==UNVISITED):print("No Path to Goal :(")
        else:
            print("Path cost is ", self.Grid[self.Goal[X]][self.Goal[Y]])
            


        
        
        


        



        