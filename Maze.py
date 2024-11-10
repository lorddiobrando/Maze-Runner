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

    def __init__(self,width,height,GoalState=None,ActorState=None,FireState=None):
        self.theMaze=maze(width,height)
        self.theMaze.CreateMaze(loopPercent=100)

        if ActorState: self.Agent=Actor(self.theMaze,ActorState)
        else: self.Agent=Actor(self.theMaze,(1,1))

        if FireState!=None:self.Fire=Actor(self.theMaze,FireState,COLOR.yellow) 
        else:self.Fire=Actor(self.theMaze,(1,width),COLOR.yellow)

        self.Grid=[[UNVISITED for i in range(width+1)] for j in range(height+1)]
        self.Functions={
            'UCS':self.UCS
        }
        self.Goal=GoalState
        self.FireQueue=deque()
        self.AgentQueue=deque()


    def  InitialiseAgent(self,cost=None):
        if(bool(self.AgentQueue)): # Check if empty. If not empty, means initialised before
            print("Error: ActorQueue already initialised :)")
            exit()
        if cost!=None:self.AgentQueue=[(cost,self.Agent.State)] 
        else:self.AgentQueue.append(self.Agent.State)

    def  InitialiseFire(self):
        if(bool(self.FireQueue)): # Check if empty. If not empty, means initialised before
            print("Error: FireQueue already initialised :)")
            exit()
        self.FireQueue.append(self.Fire.State)

    def SetGoal(self,state):self.Goal=state

    def FireSpread(self):
        #size=len(self.FireQueue)
        #for i in range(size):
            while 1:
                if self.Grid[self.FireQueue[0][X]][self.FireQueue[0][Y]]==FIRE:
                    self.FireQueue.popleft()
                else: break
            self.Fire.NowState(self.FireQueue[0])
            self.FireQueue.popleft()
            if(self.Grid[self.Fire.State[X]][self.Fire.State[Y]]==UNVISITED): 
                self.Fire.draw()
                self.Grid[self.Fire.State[X]][self.Fire.State[Y]]=FIRE
            self.FireQueue.extend(self.Fire.Actions())

    def SearchFunction(self,Key,Cost=None):
        self.Functions[Key.upper()](Cost)
        #except: print("ERROR: No function with such name :)")

    def LessGo(self,Key,CostGrid):
        if(not self.Goal or not self.Agent.State or not self.Fire.State):
            print("ERROR: Set all your States first :)")
            exit()
        self.InitialiseFire()
        self.Agent.theGUI.footprints=True
        self.Fire.theGUI.footprints=True
        self.SearchFunction(Key,CostGrid)
        self.theMaze.run()




#--------------------------------------------------------------------------
# Enter your Search Algorithms here

    def UCS(self,CostGrid=None):
        if(not CostGrid):
            print("ERROR: Chose UCS Search with no Cost Inserted :)")
            exit()
        self.InitialiseAgent(0) # Initialize cost of first node into priority queue
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]]=0
        while self.AgentQueue:
            self.FireSpread()
            CurrCost,CurrState=heappop(self.AgentQueue)
            if CurrCost>self.Grid[CurrState[X]][CurrState[Y]] or CurrCost==FIRE: continue
            print(CurrState," ",CurrCost)
            self.Agent.NowState(CurrState)
            self.Agent.draw()
            print(self.Agent.Actions())
            for state in self.Agent.Actions():
                if CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]>=self.Grid[state[X]][state[Y]]: continue
                self.Grid[state[X]][state[Y]]=CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]
                heappush(self.AgentQueue,(self.Grid[state[X]][state[Y]],state))
        if(self.Grid[self.Goal[X]][self.Goal[Y]]==UNVISITED):print("No Path to Goal :(")
        else:
            if(self.Grid[self.Goal[X]][self.Goal[Y]]!=FIRE) :print("Path to goal Costs " , self.Grid[self.Goal[X]][self.Goal[Y]])
            else: print("Sadly no path :(")


        
        
        


        



        