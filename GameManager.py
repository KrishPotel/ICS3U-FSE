from pygame import *
from enum import Enum
class GameState(Enum):
    PLAY = 0
    PAUSED = 1
    MENU = 2
    INFO=3  
    CoinSort =4
    GameOver = 5
    Difficulty=6
    WON = 7
#A lot of global varibles pretty much
class GameManager:
    def __init__(self, CurrentRoom,FinalRoom,StartRoom, screen:Surface, gameTickGetter, mouseInfoGetter, clock) -> None:
        self.CurrentRoom = CurrentRoom
        self.FinalRoom = FinalRoom
        self.StartRoom = StartRoom
        self.cameraRect = Rect(0,0,960,542)
        #All the hitboxes in th game
        self.Hitboxs = []
        self.rooms = []
        self.screen = screen
        self.gameTicks = gameTickGetter
        self.mouseInfo = mouseInfoGetter
        self.speedrunTimer = 0.0
        self.GameState = GameState.PLAY
        self.clock = clock
        self.dt = 0
        self.getTicksLastFrame = 1
    
    
    def update(self):
        #Deltatime for when the games fps will drop the player will move at the same pixel because all of the movement
        #is multipled by the time in between frames
        self.dt = (self.gameTicks() - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = self.gameTicks()
        if(self.FinalRoom.roomState == "Doors"):
            self.GameState = GameState.WON
        else:
            if(self.GameState == GameState.PLAY):
                        self.speedrunTimer += 0.01

