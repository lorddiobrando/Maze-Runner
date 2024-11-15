from Actor import * 
from pyamaze import maze,COLOR
from collections import deque
from heapq import heappop,heappush
import sys

oo=sys.maxsize
UNVISITED=oo
VISITED=1
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
            'UCS':self.UCS,
            'BFS':self.BFS,
            'IDS':self.IDS,
            'DFS':self.DFS
        }

    def __DepthLimitedSearch(self, limit):
        initial_state = self.Agent.State
        stack = deque()
        stack.append((initial_state, 0))
        par = dict()
        par[initial_state] = None
        explored = []
        while stack:
            curState, curDepth = stack.pop()
            explored.append(curState)

            if curState == self.Goal:
                path = []
                step = self.Goal
                while step is not None:
                    path.append(step)
                    step = par[step]
                path.reverse()
                print("Path is ", path)
                print("Explored nodes are ", explored)
                return 'success'
            if curDepth >= limit:
                pass
            else:
                actions = self.Agent.Actions(curState)
                for state in actions:
                    if state not in explored:
                        stack.append((state, curDepth + 1))
                        par[state] = curState
        return 'cutoff'

    def SearchFunction(self,Key,Cost=None):
        if Cost:
            self.Functions[Key.upper()](Cost)
        else:
            self.Functions[Key.upper()]()

    def Start(self,Key,CostGrid = None):
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
            if CurrCost>self.Grid[CurrState[X]][CurrState[Y]]: continue
            self.Agent.NowState(CurrState)
            for state in self.Agent.Actions(CurrState):
                if CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]>=self.Grid[state[X]][state[Y]]: continue
                self.Grid[state[X]][state[Y]]=CostGrid[state[X]][state[Y]]+self.Grid[CurrState[X]][CurrState[Y]]
                heappush(Queue,(self.Grid[state[X]][state[Y]],state))
        if(self.Grid[self.Goal[X]][self.Goal[Y]]==UNVISITED):print("No Path to Goal :(")
        else:
            print("Path cost is ", self.Grid[self.Goal[X]][self.Goal[Y]])
            
    def BFS(self, CostGrid=None):
        Queue=deque()
        Queue.append(self.Agent.State)
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]]=0
        parent = {self.Agent.State: None}
        path = []
        explored = []

        while Queue:
            CurrState=Queue.popleft()
            self.Agent.NowState(CurrState)
            explored.append(CurrState)
            if CurrState == self.Goal:
                break
            for state in self.Agent.Actions(CurrState):
                if self.Grid[state[X]][state[Y]]==UNVISITED:
                    self.Grid[state[X]][state[Y]]=self.Grid[CurrState[X]][CurrState[Y]]+1
                    parent[state] = CurrState
                    Queue.append(state)

        if self.Grid[self.Goal[X]][self.Goal[Y]]==UNVISITED:
            print("No Path to Goal :(")
        else:
            print("Path Length is ", self.Grid[self.Goal[X]][self.Goal[Y]])
            step = self.Goal
            while step is not None:
                path.append(step)
                step = parent[step]
            path.reverse()
            print("Path is ", path)
            print("Explored nodes are ", explored)



    def DFS(self, CostGrid=None):
        Stack = [(self.Agent.State, 0)]
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]] = 0
        parent = {self.Agent.State: None}
        path = []
        explored = []
        print("Begin DFS")

        while Stack:
            CurrState, CurrDepth = Stack.pop()
            if CurrState in explored:
                continue
            explored.append(CurrState)

            if CurrState == self.Goal:
                break
            self.Agent.NowState(CurrState)

            for state in self.Agent.Actions(CurrState):
                if self.Grid[state[X]][state[Y]] == UNVISITED:
                    self.Grid[state[X]][state[Y]] = CurrDepth + 1
                    parent[state] = CurrState
                    Stack.append((state, CurrDepth + 1))

        if self.Grid[self.Goal[X]][self.Goal[Y]] == UNVISITED:
            print("No Path to Goal :(")
        else:
            print("Path Length is ", self.Grid[self.Goal[X]][self.Goal[Y]])

            step = self.Goal
            while step is not None:
                path.append(step)
                step = parent[step]
            path.reverse()
            print("Path is ", path)
            print("Explored nodes are ", explored)


    def IDS(self):
        print("Begin IDS")
        max_depth = min(10000, len(self.Grid) * len(self.Grid[0]))
        for i in range(max_depth):
            print('Iteration number:', i)
            result = self.__DepthLimitedSearch(i)
            if result != 'cutoff':
                print(result)
                return result
        if (result == 'cutoff'):
            result = 'failure'
        print(result)
        return result





        
        
        


        



        
