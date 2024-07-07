from pygame import *
import Tools.tools as tools
from Units.Hitbox import Hitbox
from Sprites import *
from Tilemap import TileMap
from Units.Unit import Enemy
from Units.Unit import RangedEnemy
import GameManager

doorSprite = tools.loadImagesFromFolder("AnimatedTiles\Door")

class Door:
    def __init__(self,pos, NextRoom,gameManager:GameManager.GameManager) -> None:
        self.sprite = AnimatedSprite(pos,40,doorSprite,gameManager)
        self.gameManager = gameManager
        self.NextRoom = NextRoom
        self.doorBounds = Hitbox(Vector2(pos.x,pos.y+256),Vector2(80,80), self,self.gameManager)
        self.pos = Vector2(pos.x+64,pos.y+64)
    
    def check(self, player, gameMan):
        keys = key.get_pressed()
        self.doorBounds.update(self.pos)
        # if(keys[K_e]):
        for h in self.doorBounds.IsRectInside():
            if h.owner == player:
                if(keys[K_e]):
                    self.gameManager.CurrentRoom = self.NextRoom     
                    self.gameManager.CurrentRoom.roomState="Wave 1"
    #If I forgot to remove and fix this, this is for my sanity
    def damage(self,amount):
        return  

class Room:
    def __init__(self, tile:TileMap, RoomTransport, gameManager:GameManager, player) -> None:
        self.gameManager = gameManager
        self.gameManager.rooms.append(self)
        self.roomState = "Wave 1"
        self.map = tile
        self.wave1pos = tile.enemySpawnWave1
        self.wave2pos = tile.enemySpawnWave2
        self.wave1EnemyList = []
        self.wave2EnemyList = []
        self.RoomDict = {}
        for enemy in self.wave1pos:
            if(enemy[0] == "customTile6.png"):
                self.wave1EnemyList.append(Enemy(enemy[1], gameManager, "Player"))
            elif(enemy[0] == "customTile7.png"):
                # print(f"Ranged enemy {self} wave 1")
                self.wave1EnemyList.append(RangedEnemy(enemy[1], gameManager))
        for enemy in self.wave2pos:
            if(enemy[0] == "customTile6.png"):
                self.wave2EnemyList.append(Enemy(enemy[1], gameManager, "Player"))
            elif(enemy[0] == "customTile7.png"):
                # print(f"Ranged enemy {self} wave 2")
                self.wave2EnemyList.append(RangedEnemy(enemy[1], gameManager))
        for doors in self.map.RoomDoors:
            doors[0]=Door(doors[1], RoomTransport[0], gameManager)
            doors[1]=Door(doors[1],RoomTransport[1],gameManager)
        self.CurrentRoom = gameManager
        self.player = player
        
        self.CurrentWave1EnemyList = self.wave1EnemyList
        self.CurrentWave2EnemyList = self.wave2EnemyList


    def setNextRoom(self, doorIndex, nextRoom):
        self.map.RoomDoors[doorIndex][0] = Door(self.map.RoomDoors[doorIndex][1], nextRoom, self.gameManager)

    def Reset(self):
        self.roomState = "Wave 1"
        for e in self.CurrentWave1EnemyList:
            e.dead = False
        for e in self.CurrentWave2EnemyList:
            e.dead = False
        if(self.CurrentWave1EnemyList == []):
            for enemy in self.wave1pos:
                if(enemy[0] == "customTile6.png"):
                    self.CurrentWave1EnemyList.append(Enemy(enemy[1], self.gameManager, "Player"))
                elif(enemy[0] == "customTile7.png"):
                    # print(f"Ranged enemy {self} wave 1")
                    self.CurrentWave1EnemyList.append(RangedEnemy(enemy[1], self.gameManager))

        if(self.CurrentWave2EnemyList == []):

            for enemy in self.wave2pos:
                if(enemy[0] == "customTile6.png"):
                    self.CurrentWave2EnemyList.append(Enemy(enemy[1], self.gameManager, "Player"))
                elif(enemy[0] == "customTile7.png"):
                    # print(f"Ranged enemy {self} wave 2")
                    self.CurrentWave2EnemyList.append(RangedEnemy(enemy[1], self.gameManager))

    def runRoom(self, player):
        if(self.roomState == "Wave 1"):
            for e in self.CurrentWave1EnemyList:
                e.move(player)
                if(e.dead):
                    self.CurrentWave1EnemyList.remove(e)
                if(self.CurrentWave1EnemyList == []):
                    self.roomState = "Wave 2"
            
        if(self.roomState == "Wave 2"):
            for e in self.CurrentWave2EnemyList:
                e.move(player)
                if(e.dead):
                    self.CurrentWave2EnemyList.remove(e)
            if(self.CurrentWave2EnemyList == []):
                self.roomState = "Doors"
        
        if(self.roomState == "Doors"):
            for door in self.map.RoomDoors:
                door[0].check(self.player, self.gameManager.CurrentRoom)
                
        # if(self.roomState == "Wave 2"):