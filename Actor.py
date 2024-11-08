from pyamaze import agent,COLOR,maze
class Actor:
    def __init__(self,mz,initial_state,Color=COLOR.blue):
        self.State=initial_state
        self.theGUI=agent(mz,color=Color)
        self.Move=['E','W','N','S']
        self.HMove=[1,-1,0,0]
        self.VMove=[0,0,1,-1]
        self.Blocked=self.mz.maze_map

    def draw(self): self.theGUI.position=self.State
    def NowState(self,state):self.State=state
    def Actions(self):
        NewMoves=[]
        for i in range(4):
            NewMove=(self.State[0]+self.HMove[i],self.State[1]+self.VMove[i])
            if self.Blocked[NewMove][self.Move[i]]:
                NewMoves.append(NewMove)
        return NewMoves








