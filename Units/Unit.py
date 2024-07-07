from pygame import *
import GameManager
import Tools.tools
from Units.Hitbox import Hitbox
from Sprites import *
import Tools.tools as tools
from Units.Player import Player
from Tools.bfs import bfs
import Tools.timer

class Enemy:
    def __init__(self, position:Vector2, gameManager:GameManager.GameManager, animationPath) -> None:
        self.pos = position
        self.hitbox = Hitbox(position,Vector2(35,70), self,gameManager)
        self.tilePos=Vector2(0,0)
        self.debugPath = [(position.x,position.y), (position.x,position.y+1)]
        self.index = 1
        self.path = [Vector2(0,0)]
        self.hp = 100
        self.stoppingDistance = 64
        self.dead = False
        self.animationPath = animationPath
        self.HitTimer = Tools.timer.Timer(10)
        self.gameManager = gameManager
        self.animationManager = AnimationManager()
        self.screen = self.gameManager.screen
        animations = tools.loadImagesFromFoldersInvert(f"{self.animationPath}\Run Animation")
        a={}
        for k in animations:
            a[k]=AnimatedSprite(position,40,animations[k],gameManager)
        
        animations = tools.loadImagesFromFoldersInvert(f"{self.animationPath}\Attack", "Slash ")
        b={}
        for k in animations:
            b[k]=AnimatedSprite(position,20,animations[k],gameManager)
        
        self.animationManager.addAnimationDict(b)
        self.animationManager.addAnimationDict(a)
        self.animationManager.addAnimation("Dead", AnimatedSprite(self.pos,10,tools.loadImagesFromFolder("Player\Dead"), gameManager))
        # self.animationManager.addAnimation("Slash" ,AnimatedSprite(vec,40,tools.loadImagesFromFolder("Player\Sword Slashing\Forward")))       

        self.direction = (0,1)

        self.animationMap = {
            (1,0):"Side",
            (-1,0):"Side Inverted",
            (0,1):"Back",
            (0,-1):"Forward",
            (1,-1):"DigonalUp",
            (-1,-1):"DigonalUp Inverted",
            (1,1):"DigonalDown",
            (-1,1):"DigonalDown Inverted",
            # (0,0):"Idle"
        }

        self.SlashanimationMap = {
            (1,0):"Slash Side",
            (-1,0):"Slash Side Inverted",
            (0,1):"Slash Forward",
            (0,-1):"Slash Back",
            (1,-1):"Slash DigonalUp",
            (-1,-1):"Slash DigonalUp Inverted",
            (1,1):"Slash DigonalDown",
            (-1,1):"Slash DigonalDown Inverted",
            # (0,0):"Idle"
        }
    
    def move(self,target:Player):
        

        if(Vector2(int(self.tilePos.x), int(self.tilePos.y)) in self.gameManager.CurrentRoom.map.collide):
            print("IM IN A WALL")

        
        if(True):
            if(self.hp < 0):
                self.dead = True
            self.hitbox.update(Vector2(self.pos.x+48,self.pos.y+32))
            # self.KnightSprite.draw(self.pos)

            self.tilePos = tools.calulateTilePos(self.pos,self.gameManager)

            if(self.index < len(self.debugPath) - 1 and (self.pos - self.debugPath[self.index]).magnitude() < 4):
                self.pos = Vector2(self.debugPath[self.index][0],self.debugPath[self.index][1])
                self.index+=1
                    
            if((self.pos - target.pos).magnitude() > self.stoppingDistance):
                if(len(self.debugPath) > 0):
                    self.moveTowards(self.debugPath[self.index])
            else:
                # self.animationManager.playAnimation("Idle", self.pos)
                x = target.pos.x - self.pos.x
                y = target.pos.y - self.pos.y
                c = (x**2 + y**2)**0.5
                if c != 0:
                    self.animationManager.playMappedAnimation(self.SlashanimationMap,Vector2(round(x/c), round(y/c)), Vector2(self.pos.x+32, self.pos.y+32))
                self.attack(target)

           
            # if (self.index < len(self.debugPath)):
            #     draw.circle(self.gameManager.screen, (0,255,0), (self.debugPath[self.index][0]-self.gameManager.cameraRect.x,self.debugPath[self.index][1]-self.gameManager.cameraRect.y), 5.0)
            
            #Here we decide when to path find
            if(self.debugPath is None or self.debugPath != [] or self.debugPath == [self.pos]):
                #When the path is far away enough from the player we find a new path
                if((target.pos - self.debugPath[-1]).magnitude() > 64 or self.path == [Vector2(0,0)] or self.path == []):
                    if(self.debugPath == [self.pos]):
                        if(self.gameManager.gameTicks() % 20 == 0):
                            #the bfs is ran here
                            self.path = bfs(self.gameManager.CurrentRoom.map.collisionMap,(int(self.tilePos.x),int(self.tilePos.y)), (int(target.tilePos.x),int(target.tilePos.y)))
                    else:
                        self.path = bfs(self.gameManager.CurrentRoom.map.collisionMap,(int(self.tilePos.x),int(self.tilePos.y)), (int(target.tilePos.x),int(target.tilePos.y)))
                    if(len(self.path)-1 < self.index):
                        self.index = 0
                    self.debugPath = [tools.calulateRealPos(Vector2(x,y), self.gameManager) for x,y in self.path]
            else:
                self.debugPath = [self.pos]

            # draw.circle(self.gameManager.screen,(0,0,255), (self.pos.x-self.gameManager.cameraRect.x,self.pos.y-self.gameManager.cameraRect.y),5)
        
        else:
            self.animationManager.playAnimation("Dead", self.pos)

    #Move towards the target Vector
    def moveTowards(self, target:Vector2):
        speed=100
        x = target[0] - self.pos.x
        y = target[1] - self.pos.y
        c = (x**2 + y**2)**0.5
        if c != 0:
            self.direction = (round(x/c), round(y/c))
            self.animationManager.playMappedAnimation(self.animationMap,Vector2(round(x/c), round(y/c)), Vector2(self.pos.x+32, self.pos.y+32))
            newpos = Vector2(self.pos.x+speed*x/c* self.gameManager.dt, self.pos.y)
            newtilePos = tools.calulateTilePos(newpos, self.gameManager)
            
            if(not Vector2(int(newtilePos.x), int(newtilePos.y)) in self.gameManager.CurrentRoom.map.collide):
                self.pos.x += speed * x / c * self.gameManager.dt
            else:
                self.debugPath = [self.pos]

            newpos = Vector2(self.pos.x, self.pos.y+speed*y/c*self.gameManager.dt)
            newtilePos = tools.calulateTilePos(newpos, self.gameManager)
            
            if(not Vector2(int(newtilePos.x), int(newtilePos.y)) in self.gameManager.CurrentRoom.map.collide):
                self.pos.y += speed * y / c * self.gameManager.dt
            else:
                self.debugPath = [self.pos]
                # self.debugPath = [self.pos]
        # self.pos += (target-self.pos).normalize()*2

    def attack(self, target:Player):
        self.HitTimer.run()
        if(self.HitTimer.isFinished()):
            self.HitTimer.reset()
            target.damage(5)
        
    def damage(self, amount):
        self.hp -= amount


class RangedEnemy(Enemy):
    def __init__(self, position: tools.Vector2, gameManager: GameManager) -> None:
        super().__init__(position, gameManager, "RangedEnemy")
        self.stoppingDistance = 128

        
    def attack(self, target: Player):
        if(time.get_ticks() % 100 == 0):
            target.damage(10)