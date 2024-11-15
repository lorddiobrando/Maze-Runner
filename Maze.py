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
            'IDS':self.IDS,
            'DFS':self.DFS,
            'GREEDY':self.Greedy,
            'SA':self.SimulatedAnnealing
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
    def DFS(self, CostGrid=None):
        Stack = [(self.Agent.State, 0)]
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]] = 0
        parent = {self.Agent.State: None}
        path = []
        explored = []
        print("Begin DFS")

        while Stack:
            CurrState, CurrDepth = Stack.pop()
            if CurrState in explored:continue
            explored.append(CurrState)
            if CurrState == self.Goal:break
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
        max_depth = min(10000, len(self.Grid) * len(self.Grid[0]))
        for i in range(max_depth):
            print(i)
            result = self.__DepthLimitedSearch(i)
            if result != 'cutoff':
                print(result)
                return result
        if (result == 'cutoff'):
            result = 'failure'
        print(result)
        return result

    def __DepthLimitedSearch(self, limit):
        initial_state = self.Agent.State
        stack = deque()
        stack.append((initial_state, 0, None))
        cycle_size = 3 * limit + 1
        cycle = [None for i in range(cycle_size)]
        cycle_index = 0
        while stack:
            cur = stack.pop()
            cycle[cycle_index] = cur
            cycle_index += 1
            if cycle_index == cycle_size:
                cycle_index = 1
            if cur[0] == self.Goal:
                return 'success'
            if cur[1] >= limit:
                pass
            else:
                actions = self.Agent.Actions(cur[0])
                for state in actions:
                    flag = False
                    for tup in cycle:
                        if tup and state == tup[0]:  # checking for cycles
                            flag = True
                            break
                    if flag:
                        continue
                    stack.append((state, cur[1] + 1, cur[0]))
        return 'cutoff'

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
            for state in self.Agent.Actions(CurrState):
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
            for state in self.Agent.Actions(CurrState):
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

    def SimulatedAnnealing(self, Temp, Hkey, SchedKey):
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
            PossibleStates = self.Agent.Actions(CurrState)
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


        



        





        
        
        


        



        