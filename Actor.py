#coding:utf-8
from world import *
from util import *
from variable import (char)
print char

"""
Actor:
id
x,y
worldX,worldY
image
name
race
job
HP
MP
STR
DEF
SPD
...
これから増やす

パラメーターを増やす、減らす

monster=Actor(SOME_MONSTER,[31,11])
"""
mapX, mapY = 640 / 32, 480 / 32
class Actor():
    def __init__(self,ActorData=None,pos=None): # default argument value is mutable
        if ActorData==None:
            ActorData=[0,"None",0,"None","None",0,0,0,0,0,[]]
        if pos==None:
            pos=[0,0]
        self.act_state = -1
        self.id    = ActorData[0]
        self.name  = ActorData[1]
        self.image = ActorData[2]
        self.race  = ActorData[3]
        self.job   = ActorData[4]
        self.HP    = ActorData[5]
        self.MP    = ActorData[6]
        self.STR   = ActorData[7]
        self.DEF   = ActorData[8]
        self.SPD   = ActorData[9]
        self.state = ActorData[10]
        self.x = pos[0]
        self.y = pos[1]
        char[self.y][self.x] = self.image
class Enemy(Actor):
    def action(self,player):
        char[self.y][self.x]=-1
        def f(i):
            if i==0:
                return 1
            return i
        yMove = (player.y - self.y) / abs(f(player.y - self.y))
        xMove = (player.x - self.x) / abs(f(player.x - self.x))
        if is_movalbe(self.y+yMove,self.x+xMove)==0:
            self.x +=xMove
            self.y +=yMove
        char[self.y][self.x]=self.image

        pass

class Player(Actor):
    def action(self,key):
        self.move(key)
    def move(self,key):
        stage.drawMap(cutWorldMapToDisplay(worldMap, self.x, self.y, mapX, mapY), source="field")
        stage.drawMap(cutWorldMapToDisplay(char, self.x, self.y, mapX, mapY), "char")
        xMove, yMove = 0, 0

        if key[K_UP]:
            yMove = -1
        if key[K_DOWN]:
            yMove = 1
        if key[K_RIGHT]:
            xMove = 1
        if key[K_LEFT]:
            xMove = -1
        res=is_movalbe(self.y+yMove,self.x+xMove)
        if  res==2:
          #  time.sleep(0.1)
            stage.appendLog(u"その方向には進めない")
            return -1
        if res==1:
            """
            attack
            """
            res=self.attack(getIdFromPos(self.x+xMove,self.y+yMove))
            stage.appendLog(u"敵に"+str(res)+u"のダメージを与えた")
            time.sleep(0.1)
            return -1
        char[self.y][self.x] = -1
        self.x += xMove
        self.y += yMove
        if xMove != 0 or yMove != 0:
            stage.appendLog(str(self.name)+u"は" + str(self.x) + "," + str(self.y) + u"へ移動した")
        char[self.y][self.x] = self.image
        #stage.drawMap(cutWorldMapToDisplay(worldMap, self.x, self.y, mapX, mapY), source="field")
        #stage.drawMap(cutWorldMapToDisplay(char, self.x, self.y, mapX, mapY), "char")

        #time.sleep(0.1)
        return 1
    def attack(self,target):#,targetはid

        for actor in actors:
            if actor.id == target:
                damage=int((self.STR*(0.99)**actor.DEF))+random.randint(1,20)
                actor.HP-=damage
                if actor.HP<0:
                    actors.remove(actor)
                    char[actor.y][actor.x]=-1
                    stage.drawMap(cutWorldMapToDisplay(worldMap, self.x, self.y, mapX, mapY), source="field")
                    stage.drawMap(cutWorldMapToDisplay(char, self.x, self.y, mapX, mapY), "char")
                    stage.update()
                return damage
        return -1

