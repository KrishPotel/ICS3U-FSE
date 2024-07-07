#Main.py
#Krish Patel
#This is a isometric game losely based off the game hades the goal is to advance through each room killing all the
#eneimes in each room to advance rooms press e
#Please look at the resources.txt file for the resources I used
#It takes a little bit to turn on because it has to load a lot of maps

from pygame import *
import GameManager
from GameManager import GameState
from Units.Player import Player
from Tilemap import TileMap
from Room import Room
from coinSorting import CoinSorter
import Ui
import Tools.tools

# mixer.init()
# a = mixer.Sound("")
screen = display.set_mode((960,542))
clock = time.Clock()
# print(tileDic)
def tickGetter() -> int:
    return time.get_ticks()

def mouseInfo() -> tuple:
    mx,my=mouse.get_pos()
    click=mouse.get_pressed()
    return (mx,my,click)

def deltaTime() -> float:
    return clock.tick(120) / 1000


#Gamemanger handles a lot of the global varibles 
gameManager = GameManager.GameManager(0,0,0,screen, tickGetter,mouseInfo,deltaTime)


player = Player(Vector2(200,200),gameManager)

#Making all the tilemaps
tile1 = TileMap((0,0),"Maps\\map2")
tile2 = TileMap((0,0),"Maps\\map3")
tile3 = TileMap((0,0),"Maps\\map4")
tile4 = TileMap((0,0),"Maps\\map5")
finalTile = TileMap((0,0),"Maps\\FinalMap")
# tile4 = TileMap((0,0),"Maps\\map4")
# room2 = Room(tile3, [0,0], gameManager,player)
#Making room Objects
FinalRoom = Room(finalTile,[0,0],gameManager,player)
room3 = Room(tile3,[FinalRoom,FinalRoom], gameManager,player)
room4 = Room(tile4,[FinalRoom,FinalRoom],gameManager,player)
room2 = Room(tile2,[room3,room4], gameManager,player)
room1 = Room(tile1,[room2,room2], gameManager,player)

coinSorter = CoinSorter(screen) 
exitButton = Rect(0,442,100,100)

#Set which room to start in and the finalroom
gameManager.CurrentRoom = room1
gameManager.StartRoom = room1
gameManager.FinalRoom = FinalRoom

clock.tick(60)

player.pos = gameManager.CurrentRoom.map.Center()
index=0

gameManager.GameState = GameState.MENU

running = True
while running:
    gameManager.update()
    # print(gameManager.dt())
    # print(gameManager.CurrentRoom.wave)
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    
        
        if evt.type == KEYDOWN:
            if evt.key == K_ESCAPE:
                if(gameManager.GameState == GameState.PLAY):
                    gameManager.GameState = GameState.PAUSED
                elif(gameManager.GameState == GameState.PAUSED):
                    gameManager.GameState = GameState.PLAY
                

    
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()

    gameManager.cameraRect.x=player.pos.x-gameManager.cameraRect.width/2
    gameManager.cameraRect.y=player.pos.y-gameManager.cameraRect.height/2

    # ----------------------------------
    # screen.blit(tileDic["customTile2"], (32*0,16*0))
    # tile.s.blit(tileDic["customTile3"], (640+x*32-y*32-int(cameraRect.x), x*16+y*16-int(cameraRect.y)))

    


    #If the gamestate is play run the main game
    if(gameManager.GameState == GameState.PLAY):
        index=0
        screen.fill((29,41,81))
        #Rendering out the game map
        screen.blit(gameManager.CurrentRoom.map.toSurface(),(0-int(gameManager.cameraRect.x),0-int(gameManager.cameraRect.y)))
        screen.blit(gameManager.CurrentRoom.map.innerWall,(0-int(gameManager.cameraRect.x),0-int(gameManager.cameraRect.y)))
        # screen.blit(gameManager.CurrentRoom.map.navMeshDraw,(0-int(gameManager.cameraRect.x),0-int(gameManager.cameraRect.y)))
        player.move(gameManager.CurrentRoom.map.collide)

        #Runs the enemies
        gameManager.CurrentRoom.runRoom(player)
                   


        screen.blit(gameManager.CurrentRoom.map.wall, (0-int(gameManager.cameraRect.x),0-int(gameManager.cameraRect.y)))

        

        Ui.runUI(gameManager,player)


    elif(gameManager.GameState == GameState.PAUSED):
        Ui.runPauseMenu(gameManager,index)
        index+=1
    elif(gameManager.GameState == GameState.MENU):
        Ui.mainmenu(gameManager)
    elif(gameManager.GameState == GameState.INFO):
        Ui.InfoScreen(gameManager)
    elif(gameManager.GameState == GameState.CoinSort):
        coinSorter.run(mx,my,mb,evt)
        draw.rect(screen,(0,0,0), exitButton)

        if(exitButton.collidepoint(mx,my) and mb[0]):
            gameManager.GameState = GameState.MENU

    elif(gameManager.GameState == GameState.GameOver):
        Ui.GameOver(gameManager,player, index)
        index+=1

    elif(gameManager.GameState == GameState.Difficulty):
        Ui.difficulty(gameManager)
    elif(gameManager.GameState == GameState.WON):
        Ui.GameWon(gameManager,player,0)
        index+=1



    # ----------------------------------
    display.flip()

quit()