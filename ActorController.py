#coding:utf-8

from Actor import Actor
from Actor import Enemy
import random as rnd
class ActorController():
    def __init__(self):
        self.actors={}
        self.player=None
        pass

    def setActorAsPlayer(self,actor):
        self.player=actor

    def addActor(self,actor):
        l=[i for i in self.actors]
        newId=-1
        for n in range(len(l)+1):
            if n not in l:
                newId=n
                break
        actor.actId = newId
        self.actors.update({newId: actor})

    def delActor(self,delTarget): #actId or Actor どちらでも可
        if type(delTarget)==int:
            delId=delTarget
        if type(delTarget)==Actor or Enemy or Plaer:
            delId=delTarget.actId
        self.actors.pop(delId)


    def action(self,actor):

        tactics = [actor.tactics[i][0] for i in actor.tactics]
        weights=[actor.tactics[i][1] for i in actor.tactics]
        print(rnd.choices(tactics,weights))
        pass

param={"HP":1,"job":"test"}
actCtr=ActorController()
actCtr.addActor(Enemy(param))
actCtr.addActor(Enemy(param))
actCtr.addActor(Enemy(param))
actCtr.addActor(Enemy(param))
actCtr.addActor(Enemy(param))
actCtr.addActor(Enemy(param))

actCtr.action(actCtr.actors[1])
print([x for x in actCtr.actors])