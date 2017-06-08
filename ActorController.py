#coding:utf-8

from collections import deque
from Actor import Actor
from Actor import Enemy
from Actor import Player

import random as rnd
class ActorController():
    def __init__(self):
        self.actors={}
        self.moveQueue=deque()
        self.player=None
        self.time=1
        pass

    def setActorAsPlayer(self,player):
        if player not in self.actors:
            assert ("argument is not in self.actors")
        self.player=player
    def delActorAsPlayer(self,player):
        if player not in self.actors:
            assert("argument is not in self.actors")
        for _,actor in self.actors.items():
            if hasattr(actor,"target"):
                if actor.target==player:
                    actor.target=None

        self.player=None
        delId=player.actId
        self.actors.pop(delId)



    def addActor(self,actor,target=None):
        l=[i for i in self.actors]
        newId=-1
        for n in range(len(l)+1):
            if n not in l:
                newId=n
                break
        actor.target= target
        actor.actId = newId
        self.actors.update({newId: actor})

    def delActor(self,delTarget): #actId or Actor どちらでも可
        if type(delTarget)==int:
            delId=delTarget
        if type(delTarget)==Actor or Enemy or Plaer:
            delId=delTarget.actId
        self.actors.pop(delId)
    def getAction(self):
        if len(self.moveQueue)!=0:
            actor = self.moveQueue.popleft()
            if type(actor) == Player:
                return {"actId": actor.actId, "action": "player"}
            else:
                res = {"actId": actor.actId}
                res.update(actor.getAction())
                return res

        idList=[[x.actId,x.SPD] for _,x in self.actors.items()]
        movables = []
        while True:

            for actor in idList:
                if self.time%(1023//actor[1])==0 and actor not in movables:
                    movables.append(actor)
                #    print(self.time,1023//actor[1])
            if len(movables)==0:
                self.time=max((self.time+1)%1024,1)
                continue
            else:
                movables.sort(reverse=True,key=lambda x:x[1])
                self.moveQueue+=[self.actors[x[0]]for x in movables]
                break

        self.time = max((self.time + 1) % 1024, 1)
        actor=self.moveQueue.popleft()
        res={"actId":actor.actId}
        res.update(actor.getAction())

        return res


def getRandomParam():
    return {"HP":1,"x":20,"y":2,"job":"test","SPD":rnd.randint(30,60)}
if __name__=="__main__":
    actCtr=ActorController()
    p=Player({"SPD":15,"x":1,"y":2})
    actCtr.addActor(p)
    actCtr.setActorAsPlayer(p)
    actCtr.addActor(Enemy({"SPD":20,"x":2,"y":2}),target=self.player)
    print([x.SPD for _,x in actCtr.actors.items()])
    for i in range(100):
        request=actCtr.getAction()
        print(request)
