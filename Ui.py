from pygame import *
import GameManager
import Units.Player

font.init()

minimalPixelFont = font.Font("MinimalPixel.ttf", 32)
titleScreen = image.load("titleScreen.png")
titleScreen = transform.scale(titleScreen, (960,542))

shield = image.load("Player\deathDefies.png")
shieldScaled = transform.scale(shield,(32,32))

class Button:
    def __init__(self,rect:Rect) -> None:
        self.rect = rect
    
    def isClicked(self, gameManager:GameManager.GameManager) -> bool:
        mouse = gameManager.mouseInfo()
        if(self.rect.collidepoint(mouse[0], mouse[1]) and mouse[2][0]):
            return True
        return False
        

def drawHealthBar(x,y,screen,hp,scale, height):
    draw.rect(screen,(255,0,0), (x,y,100*scale,height))
    draw.rect(screen,(0,255,0), (x,y,hp*scale,height))
    draw.rect(screen,(0,0,0), (x,y,100*scale,height), 1)




def runUI(gameManager:GameManager.GameManager, player:Units.Player.Player):
    drawHealthBar(40,502,gameManager.screen,player.hp,2,15)

    TimerText = minimalPixelFont.render(f"{round(gameManager.speedrunTimer,2)}",True,(255,255,255))
    
    gameManager.screen.blit(TimerText,(0,0))
    infoText3 = minimalPixelFont.render("press e on yellow to continue",True,(0,0,0))
    gameManager.screen.blit(infoText3,(0,50))
    

    for i in range(player.deathDefies):
        gameManager.screen.blit(shieldScaled,(50+i*40,470))

    for enemy in gameManager.CurrentRoom.CurrentWave1EnemyList:
        drawHealthBar(enemy.pos.x-gameManager.cameraRect.x-25, enemy.pos.y-gameManager.cameraRect.y-40,gameManager.screen,enemy.hp,0.5,5)
    
    if(gameManager.CurrentRoom.roomState == "Wave 2"):
        for enemy in gameManager.CurrentRoom.CurrentWave2EnemyList:
            drawHealthBar(enemy.pos.x-gameManager.cameraRect.x-25, enemy.pos.y-gameManager.cameraRect.y-40,gameManager.screen,enemy.hp,0.5,5)

alphaSurface = Surface((960,542))
alphaSurface.set_alpha(50)
alphaSurface.fill((10,10,10))

MenuText = minimalPixelFont.render("MENU",True,(255,255,255))
Menu = Button(Rect(400,120,200,40))


def runPauseMenu(gameManager:GameManager.GameManager, index):
    if(index < 1):
        gameManager.screen.blit(alphaSurface,(0,0))

    draw.rect(gameManager.screen,(0,0,0), (400,120,200,40),0,3)
    draw.rect(gameManager.screen,(40,40,40), (400,120,200,40),2,3)

    gameManager.screen.blit(MenuText,(440,125))

    if(Menu.isClicked(gameManager)):
        gameManager.GameState = GameManager.GameState.MENU


Start = Button(Rect(100,125,220,40))
StartText = minimalPixelFont.render("START", True, (255,255,255))
Info = Button(Rect(100,225,220,40))
InfoText = minimalPixelFont.render("INFO", True, (255,255,255))
CoinSorting = Button(Rect(100,325,220,40))
CoinSortingText = minimalPixelFont.render("COIN SORT", True, (255,255,255))
Difficulty = Button(Rect(100,425,220,40))
DifficultyText = minimalPixelFont.render("Difficulty", True, (255,255,255))


menuSurface = titleScreen
# menuSurface.fill((255,255,255))

def mainmenu(gameManager:GameManager.GameManager):

    gameManager.screen.blit(titleScreen,(0,0))

    draw.rect(gameManager.screen,(0,0,0), (100,125,220,40))
    gameManager.screen.blit(StartText,(125,130))
    draw.rect(gameManager.screen,(0,0,0), (100,225,220,40))
    gameManager.screen.blit(InfoText,(125,230))
    draw.rect(gameManager.screen,(0,0,0), (100,325,220,40))
    gameManager.screen.blit(CoinSortingText,(125,330))
  

    if(Start.isClicked(gameManager)):
        gameManager.GameState = GameManager.GameState.PLAY
    if(Info.isClicked(gameManager)):
        gameManager.GameState = GameManager.GameState.INFO
    if(CoinSorting.isClicked(gameManager)):
        gameManager.GameState =GameManager.GameState.CoinSort

infoBackButtonRect = Rect(0,442,200,100)
infoBackButton = Button(infoBackButtonRect)
infoText = minimalPixelFont.render("press q to attack Kill all enemies",True,(0,0,0))
infoText2 = minimalPixelFont.render("Yellow block means door",True,(0,0,0))
infoText3 = minimalPixelFont.render("press e to continue",True,(0,0,0))
def InfoScreen(gameManager:GameManager.GameManager):
    gameManager.screen.fill((255,255,255))
    gameManager.screen.blit(infoText,(40,40))
    gameManager.screen.blit(infoText2,(40,140))
    gameManager.screen.blit(infoText3,(40,240))
    draw.rect(gameManager.screen,(0,0,0),infoBackButtonRect)
    if(infoBackButton.isClicked(gameManager)):
        gameManager.GameState = GameManager.GameState.MENU


RestartButton = Button(Rect(400,120,200,40))
RestartText = minimalPixelFont.render("Restart",True,(255,255,255))

difficultyBackButtonRect = Rect(0,442,200,100)
difficultyBackButton = Button(infoBackButtonRect)

def difficulty(gameManager:GameManager.GameManager):
    gameManager.screen.fill((255,255,255))

    draw.rect(gameManager.screen,(0,0,0),difficultyBackButtonRect)

    if(difficultyBackButton.isClicked(gameManager)):
        gameManager.GameState = GameManager.GameState.MENU




def GameOver(gameManager:GameManager.GameManager,player:Units.Player.Player, index):
    if(index < 1):
        gameManager.screen.blit(alphaSurface,(0,0))

    draw.rect(gameManager.screen,(0,0,0), (400,120,200,40))
    gameManager.screen.blit(RestartText,(440,125))

    if(RestartButton.isClicked(gameManager)):
        for room in gameManager.rooms:
            room.Reset()
        
        player.hp = 100
        player.deathDefies = 2

        gameManager.CurrentRoom = gameManager.StartRoom

        gameManager.GameState = GameManager.GameState.PLAY

def GameWon(gameManager:GameManager.GameManager,player:Units.Player.Player, index):
    if(index < 1):
        gameManager.screen.blit(alphaSurface,(0,0))

    draw.rect(gameManager.screen,(0,0,0), (400,120,200,40))
    gameManager.screen.blit(RestartText,(440,125))

    if(RestartButton.isClicked(gameManager)):
        for room in gameManager.rooms:
            room.Reset()
        
        player.hp = 100
        player.deathDefies = 3

        gameManager.CurrentRoom = gameManager.StartRoom

        gameManager.GameState = GameManager.GameState.PLAY
    


        

    
