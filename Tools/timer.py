from pygame import *

class Timer:
    def __init__(self, Seconds) -> None:
        self.timePassed = 0
        self.time = Seconds
        self.Finished = False
    
    def run(self):
        if(self.timePassed // 10 == self.time):
            self.Finished = True   
        else:
            self.timePassed+=1

    def reset(self):
        self.timePassed = 0
        self.Finished = False
    
    def isFinished(self):
        return self.Finished