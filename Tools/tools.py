#Image importing tools plus the calulations
from pygame import *
import os
import GameManager

def calulateTilePos(Vector:Vector2,gameManager:GameManager.GameManager):
    return Vector2(((Vector.x-(gameManager.CurrentRoom.map.offset+32)+(2*Vector.y))//64), (Vector.x-(gameManager.CurrentRoom.map.offset+32)-(2*Vector.y))//-64)

def calulateRealPos(Vector:Vector2,gameManager:GameManager.GameManager):
    return ((gameManager.CurrentRoom.map.offset+Vector.x*32-Vector.y*32)+32,(Vector.x*16+Vector.y*16)+16)

def loadImagesFromFolder(Path:str) -> list[Surface]:
    return [image.load(f"{Path}\\{im}") for im in os.listdir(Path)]

def loadImagesFromFolders(Path:str) -> dict[str:list[Surface]]:
    animationDict = {}
    for i in os.listdir(Path):
        animationDict[f"{i}"] = [image.load(f"{Path}\\{i}\\{im}") for im in os.listdir(f"{Path}\\{i}")]
    return animationDict

def loadImagesFromFoldersInvert(Path:str, optionalName="") -> dict[str:list[Surface]]:
    animationDict = {}
    for i in os.listdir(Path):
        animationDict[f"{optionalName}{i}"] = [image.load(f"{Path}\\{i}\\{im}") for im in os.listdir(f"{Path}\\{i}")]
        animationDict[f"{optionalName}{i} Inverted"] = [transform.flip(image.load(f"{Path}\\{i}\\{im}"),True,False) for im in os.listdir(f"{Path}\\{i}")]
    return animationDict


