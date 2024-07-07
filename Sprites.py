from pygame import *
import GameManager

class BaseSprite(sprite.Sprite):
    def __init__(self, pos:Vector2, image:Surface, gameManager:GameManager.GameManager) -> None:
        sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pos
        self.rect = Rect(pos.x,pos.y,image.get_width(), image.get_height())
        self.screen = gameManager.screen
        self.gameManager = gameManager
    
    def draw(self, pos):
        self.screen.blit(self.image,(pos.x-self.gameManager.cameraRect.x-64,pos.y-self.gameManager.cameraRect.y-64))

#Animated Sprite hand in a list of images as the last parameter
class AnimatedSprite(sprite.Sprite):
    def __init__(self, pos: Vector2, speedScale:int, imageList:list[Surface], gameManager:GameManager) -> None:
        sprite.Sprite.__init__(self)
        self.pos = pos
        self.imageList = imageList
        self.frameLen = len(imageList)
        self.index=0
        self.speed = speedScale
        self.screen = gameManager.screen
        self.gameManager = gameManager

    
    def invert(self):
        return AnimatedSprite(self.pos,self.speed,[transform.flip(image,True,False) for image in self.imageList])

    #Draws the animated sprites
    def draw(self,pos):
        if(self.index >= self.frameLen-1):
            self.index = 0
        else:
            self.index +=1
        
        self.screen.blit(self.imageList[self.gameManager.gameTicks() // self.speed % self.frameLen], (pos.x-self.gameManager.cameraRect.x-64,pos.y-self.gameManager.cameraRect.y-64))


class AnimationManager:
    def __init__(self) -> None:
        self.AnimationDict = {}
    
    def addAnimation(self,name:str, animation:AnimatedSprite):
        self.AnimationDict[name] = animation
    
    def removeAnimation(self,name:str):
        if(self.AnimationDict[name] != None):
            self.AnimationDict.pop(name)
    
    def addAnimationDict(self, di:dict[str:AnimatedSprite]):
        self.AnimationDict.update(di)

    def playAnimation(self, name:str, pos:Vector2):
        self.AnimationDict[name].draw(pos)

    def playMappedAnimation(self, map,direction:Vector2, pos:Vector2):
        for key in map:
            if(key == (direction.x,direction.y)):
                self.playAnimation(map[key],pos)