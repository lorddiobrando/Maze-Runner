from Actor import * 
from pyamaze import maze
from collections import deque
from heapq import heappop,heappush
import sys
import random
import math

oo=sys.maxsize
UNVISITED=oo
VISITED=1
X=0
Y=1



class Maze:

    def __init__(self,height,width,GoalState=None,ActorState=(1,1)):
        self.theMaze=maze(height,width)
        self.theMaze.CreateMaze(loopPercent=50)
        self.Agent=Actor(self.theMaze,ActorState)
        self.Size=(width,height)
        if GoalState==None:self.Goal=(height,width)
        else: self.Goal=GoalState

        self.Grid=[[UNVISITED for i in range(width+1)] for j in range(height+1)]
        
        self.Functions={
            'UCS':self.UCS,
            'BFS':self.BFS,
            'GREEDY':self.Greedy,
            'SA':self.SA
        }

        self.HFunctions={
            'MANHATTEN':self.Manhatten

        }
        self.SchedFunctions={
            'LINEAR':self.Linear
        }

    def Path(self,Parent):
            step=self.Goal
            path=[]
            while step is not None:
                path.append(step)
                step = Parent[step]
            path.reverse()
            return path

    def SearchFunction(self,Key,Cost=None,HKey=None, SchedKey=None, Temp=None):
        if Cost: self.Functions[Key.upper()](Cost)
        elif HKey and not SchedKey: self.Functions[Key.upper()](HKey)
        elif SchedKey: self.Functions[Key.upper()](Temp,HKey,SchedKey)
        else: self.Functions[Key.upper()]()

    def HeuristicFunction(self,Key):
        return self.HFunctions[Key.upper()]()
    
    def ScheduleFunction(self,Key,Temp):
        return self.SchedFunctions[Key.upper()](Temp)
    
    def Start(self,Key,CostGrid = None,HKey=None,SchedKey=None, Temp= None):
        if(not self.Goal or not self.Agent.State):
            print("ERROR: Set all your States first :)")
            exit()
        self.Agent.theGUI.footprints=True
        if CostGrid:self.SearchFunction(Key,CostGrid)
        elif HKey and not SchedKey: self.SearchFunction(Key,HKey=HKey)
        elif SchedKey: self.SearchFunction(Key,HKey = HKey,SchedKey=SchedKey, Temp=Temp)
        else:self.SearchFunction(Key)
        self.theMaze.run()

# Heuristic Functions Here
    def Manhatten(self):
            CostGrid=[]
            for i in range(self.Size[X]+1):
                row=[]
                for j in range(self.Size[Y]+1):
                    row.append(abs(self.Goal[Y]-j)+abs(self.Goal[X]-i))
                CostGrid.append(row)
            return CostGrid 
    
# Schedueling Functions Here
    def Linear(self,Temp):
        return max(0.01, min(1, 1 - 0.001 * Temp))



# Search Algorithms here

    def UCS(self,CostGrid=None):
        parent = {self.Agent.State: None}
        Queue=[(0,self.Agent.State)]
        print("Begin")
        if(not CostGrid):
            print("ERROR: Chose UCS Search with no Cost Inserted :)")
            exit()
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]]=0
        while Queue:
            CurrCost,CurrState=heappop(Queue)
            if CurrCost>self.Grid[CurrState[X]][CurrState[Y]]: continue
            self.Agent.NowState(CurrState)
            for state in self.Agent.Actions():
                if CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]>=self.Grid[state[X]][state[Y]]: continue
                self.Grid[state[X]][state[Y]]=CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]
                parent[state] = CurrState
                heappush(Queue,(self.Grid[state[X]][state[Y]],state))
        if(self.Grid[self.Goal[X]][self.Goal[Y]]==UNVISITED):print("No Path to Goal :(")
        else:
            print("Path cost is ", self.Grid[self.Goal[X]][self.Goal[Y]])
            print("Path is ", self.Path(parent))

            
    def BFS(self):
        Queue=deque()
        Queue.append(self.Agent.State)
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]]=0
        parent = {self.Agent.State: None}
        explored = []

        while Queue:
            CurrState=Queue.popleft()
            self.Agent.NowState(CurrState)
            explored.append(CurrState)
            if CurrState == self.Goal:
                break
            for state in self.Agent.Actions():
                if self.Grid[state[X]][state[Y]]==UNVISITED:
                    self.Grid[state[X]][state[Y]]=self.Grid[CurrState[X]][CurrState[Y]]+1
                    parent[state] = CurrState
                    Queue.append(state)

        if self.Grid[self.Goal[X]][self.Goal[Y]]==UNVISITED:
            print("No Path to Goal :(")
        else:
            print("Path Length is ", self.Grid[self.Goal[X]][self.Goal[Y]])
            print("Explored nodes are ", explored)
            print("Path is ",self.Path(parent))
    
    def Greedy(self,HKey):
        CostGrid=self.HeuristicFunction(HKey)
        print(CostGrid)
        self.SearchFunction('UCS',CostGrid)

    def SA(self, Temp, Hkey, SchedKey):
        CurrState = self.Agent.State
        Parent = {self.Agent.State: None}
        CostGrid = self.HeuristicFunction(Hkey)
        CurrValue = CostGrid[CurrState[X]][CurrState[Y]]
        Explored = set()
        T = 0
        while True:
            T += 1
            Temp = self.ScheduleFunction(SchedKey, T)
            if CurrState == self.Goal or Temp <= 0.01:
                break
            PossibleStates = self.Agent.Actions()
            while True: 
                NextState = random.choice(PossibleStates)
                NextValue = CostGrid[NextState[X]][NextState[Y]]
                Delta = CurrValue - NextValue
                if Delta > 0 or random.random() < math.exp(-Delta / Temp):
                    if NextState not in Parent:
                         Parent[NextState] = CurrState
                    CurrState = NextState
                    CurrValue = NextValue
                    if CurrState not in Explored:
                        Explored.add(CurrState)
                    self.Agent.NowState(CurrState)
                    break
        if CurrState == self.Goal:
            print("Path is ", self.Path(Parent))
        else:
            print("No Path to Goal :(")


        



        





        
        
        


        



        