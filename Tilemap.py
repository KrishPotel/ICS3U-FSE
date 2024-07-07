#Importer code for the tiled jsons

from pygame import *
import json
import pprint

#We need a offset to place isometric tilesets here we calulate it
def getOffsetfromTiledJson(jsonPath):
   
    f = open(f"{jsonPath}.json")
    tileMap = json.load(f)

    w = tileMap["layers"][0]["width"]
    h = tileMap["layers"][0]["height"]
    offset =  32*h
    return offset

#Gets the drawable surface
def getLayerfromTiledJson(jsonPath, num):
   
    f = open(f"{jsonPath}.json")
    tileMap = json.load(f)
    
    TilesDic = {}
    for i in tileMap["tilesets"][0]["tiles"]:
        s = i["image"][i["image"].find("c"):]
        # print(f"Tiles\\{s}")
        TilesDic[i["id"]+1] = image.load(f"Tiles\\{s}")
    w = tileMap["layers"][0]["width"]
    h = tileMap["layers"][0]["height"]
    offset = getOffsetfromTiledJson(jsonPath)
    layerSurface = Surface((10000,10000))

    layerSurface.fill((255,255,255))

    layerSurface.set_colorkey((255,255,255))
    
    Ground = []

    #Spilt the 1d list tiled spits out into a readable 2dList
    for y in range(0,tileMap["layers"][num]["width"]*h, w):
        
        a = [tileMap["layers"][num]["data"][x] for x in range(y,y+w,1)]

        Ground.append(a)
    
    for y in range(0,len(Ground),1):
        for x in range(len(Ground[y])):
            if(Ground[y][x]!=0):
                layerSurface.blit(TilesDic[Ground[y][x]], (offset+x*32-y*32,x*16+y*16))

    return layerSurface

#All the collision vectors which are walls in the collision layer
def getCollisonVectorsfromTiledJson(jsonPath, num):
   
    f = open(f"{jsonPath}.json")
    tileMap = json.load(f)
    
    Ground = []
    CollisionLayer = []
    w = tileMap["layers"][0]["width"]
    h = tileMap["layers"][0]["height"]

    for y in range(0,tileMap["layers"][num]["width"]*h, w):
        
        a = [tileMap["layers"][num]["data"][x] for x in range(y,y+30,1)]

        Ground.append(a)
    
    for y in range(0,len(Ground),1):
        for x in range(len(Ground[y])):
            if(Ground[y][x]!=0):
                CollisionLayer.append(Vector2(x,y))

    return CollisionLayer

#Gets the enemy type and wave spawn location
def getWavefromTiledJson(jsonPath, num):
   
    f = open(f"{jsonPath}.json")
    tileMap = json.load(f)

    w = tileMap["layers"][0]["width"]
    h = tileMap["layers"][0]["height"]
    offset = getOffsetfromTiledJson(jsonPath)

    TilesDic = {}
    for i in tileMap["tilesets"][0]["tiles"]:
        s = i["image"][i["image"].find("c"):]
        TilesDic[i["id"]+1] = s

    
    Ground = []
    pos=[]

    for y in range(0,tileMap["layers"][num]["width"]*h, w):
        
        a = [tileMap["layers"][num]["data"][x] for x in range(y,y+30,1)]

        Ground.append(a)
    
    for y in range(0,len(Ground),1):
        for x in range(len(Ground[y])):
            if(Ground[y][x]!=0):
                pos.append([TilesDic[Ground[y][x]], Vector2(offset+x*32-y*32,x*16+y*16)])

    return pos



#
def getCollisonMapfromTiledJson(jsonPath, num):
   
    f = open(f"{jsonPath}.json")
    tileMap = json.load(f)
    w = tileMap["layers"][0]["width"]
    h = tileMap["layers"][0]["height"]
    Ground = []

    for y in range(0,tileMap["layers"][num]["width"]*h, w):
        
        a = [tileMap["layers"][num]["data"][x] for x in range(y,y+30,1)]

        Ground.append(a)

    return Ground




def getMapfromTiledJson(jsonPath):
    
    f = open(f"{jsonPath}.json")
    tileMap = json.load(f)

    TilesDic = {}
    for i in tileMap["tilesets"][0]["tiles"]:
        s = i["image"][i["image"].find("c"):]
        TilesDic[i["id"]+1] = image.load(f"Tiles\\{s}")

    groundSurface = getLayerfromTiledJson(jsonPath, 0)
    wallSurface = getLayerfromTiledJson(jsonPath,2)
    innerWallSurface = getLayerfromTiledJson(jsonPath,1)
    navMash = getCollisonMapfromTiledJson(jsonPath, 4)
    navMeshDraw = getLayerfromTiledJson(jsonPath,4)
    collisons = getCollisonVectorsfromTiledJson(jsonPath, 3)
    enemySpwanWave1 = getWavefromTiledJson(jsonPath, 5)
    enemySpwanWave2 = getWavefromTiledJson(jsonPath, 6)
    Roomdoors = getWavefromTiledJson(jsonPath,7 )
    offset = getOffsetfromTiledJson(jsonPath)

    return groundSurface, wallSurface,innerWallSurface,collisons,navMash,enemySpwanWave1,enemySpwanWave2,Roomdoors,offset,navMeshDraw

class TileMap:
    def __init__(self, position: Vector2, Path:str) -> None:
        self.pos = position
        self.surface, self.wall,self.innerWall,self.collide,self.collisionMap,self.enemySpawnWave1,self.enemySpawnWave2,self.RoomDoors,self.offset,self.navMeshDraw = getMapfromTiledJson(Path)
        self.SurfaceWidth = self.surface.get_width()
        self.SurfaceHeight = self.surface.get_height()
        self.tilemapZero = Vector2(640,0)

    
    def toSurface(self) -> Surface:
        return self.surface
    

    def Center(self) -> Vector2:
        return Vector2(self.offset+200, 400)

class Room:
    def __init__(self, tile) -> None:
        self.roomState = "Wave 1"
        self.map = tile

