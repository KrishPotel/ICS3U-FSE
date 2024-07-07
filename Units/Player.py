from pygame import *
import GameManager
from Units.Hitbox import Hitbox
from Tools.timer import Timer
from Sprites import *
import Tools.tools as tools

class Player:
    def __init__(self,position:Vector2, gameManager:GameManager.GameManager) -> None:
        #Setting player constants
        self.moving = True
        self.Hitbox = Hitbox(position, Vector2(35,70), self,gameManager)
        self.HurtBox = Hitbox(position,Vector2(35,40), self,gameManager)
        self.pos=position
        self.tilePos=Vector2(0,0)
        self.velocity=Vector2(0,0)

        #Amount of times you can die
        self.deathDefies = 3

        
        self.gameManager = gameManager

        self.damageResPercent= 90
        self.AttackBonusPercent = 5

        
        self.hp = 100
        self.attacking = False
        self.DashTimer = Timer(50)
        self.ImmunityTimer = Timer(10)
        self.direction = Vector2(0,1)

        #Define animation manager
        self.animationManager = AnimationManager()
        animations = tools.loadImagesFromFoldersInvert("Player\Run Animation")
        a={}
        for k in animations:
            a[k]=AnimatedSprite(position,40,animations[k], gameManager)
        
        animations = tools.loadImagesFromFoldersInvert("Player\Attack", "Slash ")
        b={}
        for k in animations:
            b[k]=AnimatedSprite(position,20,animations[k],gameManager)
        
        animations = tools.loadImagesFromFoldersInvert("Player\Idle Animation", "Idle ")
        c={}
        for k in animations:
            c[k]=AnimatedSprite(position,20,animations[k],gameManager)
        
        animations = tools.loadImagesFromFoldersInvert("Player\Idle Animation", "Dash ")
        d={}
        for k in animations:
            d[k]=AnimatedSprite(position,20,animations[k],gameManager)
        
        self.animationManager.addAnimationDict(a)
        self.animationManager.addAnimationDict(b)
        self.animationManager.addAnimationDict(c)
        # self.animationManager.addAnimationDict(d)
        self.keyTimer = Timer(5)
        self.index = 0
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

        self.IdleanimationMap = {
            (1,0):"Idle Side",
            (-1,0):"Idle Side Inverted",
            (0,1):"Idle Forward",
            (0,-1):"Idle Back",
            (1,-1):"Idle DigonalUp",
            (-1,-1):"Idle DigonalUp Inverted",
            (1,1):"Idle DigonalDown",
            (-1,1):"Idle DigonalDown Inverted",
            # (0,0):"Idle"
        }

        # self.DashanimationMap = {
        #     (1,0):"Dash Side",
        #     (-1,0):"Dash Side Inverted",
        #     (0,1):"Dash Forward",
        #     (0,-1):"Dash Back",
        #     (1,-1):"Dash DigonalUp",
        #     (-1,-1):"Dash DigonalUp Inverted",
        #     (1,1):"Dash DigonalDown",
        #     (-1,1):"Dash DigonalDown Inverted",
        #     # (0,0):"Idle"
        # }

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
    
    def move(self, collide):
        #Immunity so the player doesn't die instantly
        self.ImmunityTimer.run()
        #Update hitboxs
        self.Hitbox.update(Vector2(self.pos.x+15,self.pos.y))
        self.HurtBox.update(Vector2(self.pos.x+self.direction.x*20+10,self.pos.y+self.direction.y*20+10))
        speed = 150

        # self.tilePos = Vector2((self.pos.x-672+(2*self.pos.y))//64, (self.pos.x-672-(2*self.pos.y))//-64)
        self.tilePos = tools.calulateTilePos(self.pos, self.gameManager)
        self.tilePos.x-=1
        # print(self.tilePos,self.otherTilepos)

        keys = key.get_pressed()

        self.keyTimer.run()
        if(self.velocity != Vector2(0,0) and self.keyTimer.isFinished()):
            self.direction = self.velocity.copy()
            self.keyTimer.reset()
        
        if(keys[K_w]):
            self.velocity.y=-1
            self.index = 0
        elif(keys[K_s]):
            self.velocity.y=1
            self.index = 0
        else:
            self.velocity.y =0

        if(keys[K_d]):
            self.velocity.x=1
            self.index = 0
        elif(keys[K_a]):
            self.velocity.x=-1
        else:          
            self.velocity.x =0
        
        if(keys[K_q]):
            self.animationManager.playMappedAnimation(self.SlashanimationMap,Vector2(self.direction.x, self.direction.y),self.pos)
            self.attacking = True
            self.attack()
        # elif(not self.DashTimer.isFinished()):
            # self.animationManager.playMappedAnimation(self.DashanimationMap,self.velocity,self.pos)
        elif(self.velocity == Vector2(0,0)):
            self.animationManager.playMappedAnimation(self.IdleanimationMap,self.direction,self.pos)
        else:
            self.attacking = False
            self.animationManager.playMappedAnimation(self.animationMap,self.velocity,self.pos)


        if(self.velocity.x != 0 and self.velocity.y != 0):
            self.velocity.normalize()
        
        self.DashTimer.run()
        
        if(keys[K_SPACE] and self.DashTimer.isFinished()):
            newpos = Vector2(self.pos.x+(self.velocity.x*400*self.gameManager.dt),self.pos.y+(self.velocity.y*400*self.gameManager.dt))
            newtilePos = tools.calulateTilePos(newpos, self.gameManager)
            newtilePos.x-=1
        else:
            #If the newtile hits a wall it doesn't move it does it moves
            newpos = Vector2(self.pos.x+self.velocity.x*speed*self.gameManager.dt,self.pos.y+self.velocity.y*speed*self.gameManager.dt)
            newtilePos = tools.calulateTilePos(newpos, self.gameManager)
            newtilePos.x-=1
        if(newtilePos not in collide):
            if(keys[K_SPACE] and self.DashTimer.isFinished()):
                self.pos.x += self.velocity.x*400*self.gameManager.dt
                print("dashing")
                self.pos.y += self.velocity.y*400*self.gameManager.dt
                self.DashTimer.reset()
            else:
                self.pos.x += self.velocity.x*speed*self.gameManager.dt
                self.pos.y += self.velocity.y*speed*self.gameManager.dt

        # print(self.pos,self.velocity)
    
    def damage(self, amount):
        #Damage is handled by the unit because it makes it easier to calulate resistances
        if(self.hp < 0):
            if(self.deathDefies > 0):
                self.hp=100
                self.deathDefies-=1
            else:
                self.gameManager.GameState = GameManager.GameState.GameOver

        if(self.ImmunityTimer.isFinished()):
            self.hp -= amount * self.damageResPercent/100
            self.ImmunityTimer.reset()

    def attack(self):
        for h in self.HurtBox.IsRectInside():
            if(h.owner != self):
                if(time.get_ticks() % 10 == 0):
                    h.owner.damage(5)