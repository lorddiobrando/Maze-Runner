from Actor import * 
from pyamaze import maze
from collections import deque
from heapq import heappop,heappush
import sys
import random
import math
import numpy as np
import time
oo=sys.maxsize
UNVISITED=oo
VISITED=1
X=0
Y=1

class Maze:

    def __init__(self,height,width,GoalState=None,ActorState=(1,1), delay = 10):
        self.theMaze=maze(height,width)
        if GoalState==None:self.Goal=(height,width)
        else: self.Goal=GoalState
        self.theMaze.CreateMaze(self.Goal[0],self.Goal[1],loopPercent=30)
        self.Agent=Actor(self.theMaze,ActorState)
        self.PathAgent = agent(self.theMaze, ActorState[0], ActorState[1], footprints = True, filled=True, color = 'red')
        self.ExploredAgent = agent(self.theMaze, ActorState[0], ActorState[1], footprints = True, filled=True, color = 'green')
        self.Size=(width,height)
        self.Grid=[[UNVISITED for i in range(width+1)] for j in range(height+1)]
        self.delay = delay
        self.Functions={
            'UCS':self.UCS,
            'BFS':self.BFS,
            'IDS':self.IDS,
            'DFS':self.DFS,
            'GREEDY':self.Greedy,
            'SA':self.SimulatedAnnealing,
            'ASTAR':self.AStar,
            'HC':self.HillClimbing,
            'GA':self.GeneticSearch
        }

        self.HFunctions={
            'MANHATTEN':self.Manhatten,
            'EUCLEDIAN':self.Eucledian

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

    def Start(self,Key, pop_size = None, iterations = 10000,CostGrid=None,HKey=None, SchedKey=None, Temp=None):
        if CostGrid and not HKey: self.Functions[Key.upper()](CostGrid)
        elif HKey and not SchedKey and not CostGrid: self.Functions[Key.upper()](HKey)
        elif HKey and CostGrid: self.Functions[Key.upper()](CostGrid,HKey)
        elif SchedKey: self.Functions[Key.upper()](HKey,SchedKey)
        elif pop_size: self.Functions[Key.upper()](pop_size, iterations)
        else: self.Functions[Key.upper()]()
        self.theMaze.run()

    def HeuristicFunction(self,Key):
        return self.HFunctions[Key.upper()]()
    
    def ScheduleFunction(self,Key,Temp):
        return self.SchedFunctions[Key.upper()](Temp)
    
    # def Start(self,Key, pop_size = None, iterations = 10000, CostGrid = None,HKey=None,SchedKey=None, Temp= None):
    #     if(not self.Goal or not self.Agent.State):
    #         print("ERROR: Set all your States first :)")
    #         exit()
    #     if CostGrid and not HKey:self.SearchFunction(Key, Cost = CostGrid)
    #     elif HKey and not SchedKey and not CostGrid: self.SearchFunction(Key,HKey=HKey)
    #     elif HKey and CostGrid: self.SearchFunction(Key,HKey=HKey,Cost=CostGrid)
    #     elif SchedKey: self.SearchFunction(Key,HKey = HKey,SchedKey=SchedKey, Temp=Temp)
    #     elif pop_size: self.SearchFunction(Key,pop_size = pop_size,iterations = iterations)
    #     else:self.SearchFunction(Key)
    #     self.theMaze.run()

    # Heuristic Functions Here
    def Manhatten(self):
            CostGrid=[]
            for i in range(self.Size[X]+1):
                row=[]
                for j in range(self.Size[Y]+1):
                    row.append(abs(self.Goal[Y]-j)+abs(self.Goal[X]-i))
                CostGrid.append(row)
            return CostGrid 

    def Eucledian(self):
            CostGrid=[]
            for i in range(self.Size[X]+1):
                row=[]
                for j in range(self.Size[Y]+1):
                    row.append(math.sqrt((self.Goal[Y]-j)**2+abs(self.Goal[X]-i)**2))
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
            print("Path is ", self.Path(parent))
            print("Explored nodes are ", explored)
            self.theMaze.tracePath({ self.ExploredAgent: explored}, delay = self.delay)
            self.theMaze.tracePath({ self.PathAgent: self.Path(parent)}, delay = self.delay)

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
                print("Path is ", self.Path(par))
                print("Explored nodes are ", explored)
                self.theMaze.tracePath({ self.ExploredAgent: explored}, delay = self.delay)
                self.theMaze.tracePath({ self.PathAgent: self.Path(par)}, delay = self.delay)
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

    def UCS(self,CostGrid=None):
        parent = {self.Agent.State: None}
        Queue=[(0,self.Agent.State)]
        explored = []
        print("Begin")
        if(not CostGrid):
            print("ERROR: Chose UCS Search with no Cost Inserted :)")
            exit()
        self.Grid[self.Agent.State[X]][self.Agent.State[Y]]=0
        while Queue:
            CurrCost,CurrState=heappop(Queue)
            if CurrCost>self.Grid[CurrState[X]][CurrState[Y]]: continue
            explored.append(CurrState)
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
            self.theMaze.tracePath({ self.ExploredAgent: explored}, delay = self.delay)
            self.theMaze.tracePath({ self.PathAgent: self.Path(parent)}, delay = self.delay)

        

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
            self.theMaze.tracePath({ self.ExploredAgent: explored}, delay = self.delay)
            self.theMaze.tracePath({ self.PathAgent: self.Path(parent)}, delay = self.delay)
    
    def Greedy(self,HKey):
        start=time.time()
        h=self.HeuristicFunction(HKey)
        parent = {self.Agent.State: None}
        Queue=[(0,self.Agent.State)]
        explored = []
        if(not h):
            print("ERROR: Chose Greedy Search with no heuristic Inserted :)")
            exit()
        while Queue:
            _,CurrState=heappop(Queue)
            if CurrState==self.Goal: break
            self.Grid[CurrState[X]][CurrState[Y]]=VISITED
            explored.append(CurrState)
            for state in self.Agent.Actions(CurrState):
                if self.Grid[state[X]][state[Y]]==VISITED: continue
                parent[state] = CurrState
                heappush(Queue,(h[state[X]][state[Y]],state))
            # print("Path cost is ", self.Grid[self.Goal[X]][self.Goal[Y]])
            # print("Path is ", self.Path(parent))
        finish=time.time()
        print(finish," - ",time.time())
        print("Time taken: ",(finish-start)*1e6," Microseconds")
        print("Explored nodes are ", len(explored))
        self.theMaze.tracePath({ self.ExploredAgent: explored}, delay = 10)
        self.theMaze.tracePath({ self.PathAgent: self.Path(parent)}, delay = 10)
    
    def AStar(self,CostGrid,HKey):
        start=time.time()
        h=self.HeuristicFunction(HKey)
        parent = {self.Agent.State: None}
        Queue=[(0,self.Agent.State)]
        explored = []
        if(not CostGrid or not h):
            print("ERROR: Chose UCS Search with no Cost Inserted :)")
            exit()
        while Queue:
            _,CurrState=heappop(Queue)
            if CurrState==self.Goal: break
            self.Grid[CurrState[X]][CurrState[Y]]=VISITED
            explored.append(CurrState)
            for state in self.Agent.Actions(CurrState):
                if self.Grid[state[X]][state[Y]]==VISITED: continue
                parent[state] = CurrState
                heappush(Queue,(CostGrid[state[X]][state[Y]]+h[state[X]][state[Y]],state))
            # print("Path cost is ", self.Grid[self.Goal[X]][self.Goal[Y]])
            # print("Path is ", self.Path(parent))
        finish=time.time()
        print(finish," - ",time.time())
        print("Time taken: ",(finish-start)*1e6," Microseconds")
        print("Explored nodes are ", len(explored))
        self.theMaze.tracePath({ self.ExploredAgent: explored}, delay = 10)
        self.theMaze.tracePath({ self.PathAgent: self.Path(parent)}, delay = 10)
     

    def SimulatedAnnealing(self, Hkey, SchedKey, Temp = None):
        CurrState = self.Agent.State
        Parent = {self.Agent.State: None}
        CostGrid = self.HeuristicFunction(Hkey)
        CurrValue = CostGrid[CurrState[X]][CurrState[Y]]
        Explored = []
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
                        Explored.append(CurrState)
                    self.Agent.NowState(CurrState)
                    break
        if CurrState == self.Goal:
            print("Path is ", self.Path(Parent))
            print("Explored nodes are ", Explored)
            self.theMaze.tracePath({ self.ExploredAgent: list(Explored)}, delay = self.delay)
            self.theMaze.tracePath({ self.PathAgent : self.Path(Parent)}, delay = self.delay)
        else:
            self.theMaze.tracePath({self.ExploredAgent: list(Explored)}, delay=10)
            print("No Path to Goal :(")

    def __NodalHeuristic(self, state):
        # Manhatten distance
        dist = abs(state[0] - self.Goal[0]) + abs(state[1] - self.Goal[1])
        return dist

    def HillClimbing(self):
        CurrState = self.Agent.State
        path = list()
        path.append(CurrState)
        flag = True
        while flag:
            flag = False
            for state in self.Agent.Actions(CurrState):
                if self.__NodalHeuristic(state) < self.__NodalHeuristic(CurrState):
                    flag = True
                    CurrState = state
            if flag:
                path.append(CurrState)

        print("Path is ", path)
        self.theMaze.tracePath({self.ExploredAgent: path}, delay=10)
        
    def __InitialisePopulation(self, pop_size):
        height_length = len(str(len(self.Grid) - 1))
        width_length = len(str(len(self.Grid[0]) - 1))

        pop = list()
        for i in range(pop_size):
            chromosome = str()
            for num in np.random.choice(range(0, 10), height_length):
                chromosome += str(num)

            for num in np.random.choice(range(0, 10), width_length):
                chromosome += str(num)

            pop.append(chromosome)
        return pop

    def __Fitness(self, pop):
        fitness_vals = list()
        encoded_goal = str(self.Goal[0]) + str(self.Goal[1])

        for chromosome in pop:
            fitness = sum([9 - abs(int(chromosome[i]) - int(encoded_goal[i])) for i in range(len(encoded_goal))])
            # fitness = sum([1 if chromosome[i] == encoded_goal[i] else 0 for i in range(len(encoded_goal))])
            fitness_vals.append(fitness)

        prop = list()
        den = sum(fitness_vals)
        if den:
            for i in range(len(fitness_vals)):
                prop.append(fitness_vals[i] / den)
        else:
            for i in range(len(fitness_vals)):
                prop.append(0)

        rem = 1 - sum(prop)
        rem /= len(prop)

        for i in range(len(fitness_vals)):
            prop[i] += rem
        return prop

    def __Reproduce(self, x, y):
        toggle = 0
        offspring = str()
        for i in range(len(x)):
            if (toggle % 2) == 0:
                offspring += x[i]
            else:
                offspring += y[i]
            toggle += 1
        return offspring

    def __Mutate(self, offspring, prop = 0.2):
        mutations = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        index = np.random.choice(range(len(offspring)), 1)[0]

        temp = list(offspring)
        if np.random.random() < prop:
            temp[index] = np.random.choice(mutations, 1)[0]
            offspring = ''.join(temp)

        return offspring


    def GeneticSearch(self, pop_size, iterations):
        pop = self.__InitialisePopulation(pop_size)
        encoded_goal = str(self.Goal[0]) + str(self.Goal[1])
        generation = 1
        while iterations:
            print('Generation:', generation)
            print(pop)
            generation += 1
            if encoded_goal in pop:
                print('success')
                return
            new_pop = list()
            prop = self.__Fitness(pop)
            while len(new_pop) < pop_size:
                x = str(np.random.choice(pop, 1, prop)[0])
                y = str(np.random.choice(pop, 1, prop)[0])
                offspring = self.__Reproduce(x, y)
                offspring = self.__Mutate(offspring, 0.1)
                new_pop.append(offspring)
            pop = new_pop
            iterations -= 1
        print('failure')
        return



        
        
        


        




        