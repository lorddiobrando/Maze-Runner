from pyamaze import agent,COLOR
class Actor:
    def __init__(self,mz,initial_state,func=None,Color=COLOR.blue):
        self.State=initial_state
        self.TransFunc=func
        self.theGUI=agent(mz,color=Color)
    
    def draw(self,state): self.theGUI.position=state

    def SetTransition(self,func):
        self.TransFunc=func

    def Transition(self):
        if(not self.TransFunc): 
            print("ERROR: Set your function first please :)")
            exit()
        self.TransFunc()


