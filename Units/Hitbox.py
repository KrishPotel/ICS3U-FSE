from pygame import *
import GameManager
#Very simple hitboxs checks if it's rect collides with the other rect that are stored in the gameManager
#I could've made it a set to make it more effiecent
class Hitbox:
    def __init__(self, vec:Vector2, size:Vector2, Owner, gameManager:GameManager.GameManager) -> None:
        gameManager.Hitboxs.append(self)
        self.pos = vec
        self.size = size
        self.r = Rect(vec.x,vec.y,size.x,size.y)
        self.owner = Owner
        self.gameManager = gameManager
    
    def update(self, pos:Vector2):
        self.r = Rect(pos.x-self.gameManager.cameraRect.x-64,pos.y-self.gameManager.cameraRect.y-64,self.size.x,self.size.y)
        draw.rect(self.gameManager.screen,(0,0,0), self.r ,1)
    
    #Checks if the rect is inside of the other rects
    def IsRectInside(self):
        colliding = []
        for hitbox in self.gameManager.Hitboxs:
            if(self.r.colliderect(hitbox.r)):
                colliding.append(hitbox)
        return colliding