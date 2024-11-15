from pyamaze import agent,COLOR,maze
class Actor:
    def __init__(self,mz,initial_state,Color=COLOR.blue):
        self.State=initial_state
        self.theGUI=agent(mz,color=Color)
        self.Move=['E','W','N','S']
        self.HMove=[1,-1,0,0]
        self.VMove=[0,0,-1,1]
        self.Blocked=mz.maze_map

    def draw(self,Color=None):
        if(Color):
            self.theGUI.position=self.State
        else:
            self.GoalGui=agent()

    def NowState(self, state):self.State=state
    def Actions(self, state):
        NewMoves=[]
        for i in range(4):
            if self.Blocked[state][self.Move[i]]:
                NewMove=(state[0]+self.VMove[i], state[1]+self.HMove[i])
                NewMoves.append(NewMove)
        return NewMoves








