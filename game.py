#coding:utf-8

from ActorController import ActorController
from Actor import Player,Enemy,Actor
from map import Map
class game():
    def __init__(self,actorCtr,fieldMap):
        self.actorCtr=actorCtr
        self.fieldMap=fieldMap


actCtr=ActorController()
p=Player({"SPD":10,"HP":10,"STR":5,"DEF":5,"x":5,"y":5})
actCtr.addActor(p)
actCtr.setActorAsPlayer(p)
actCtr.addActor(Enemy({"SPD":10,"HP":10,"STR":5,"DEF":5,"x":9,"y":9,"dist":1}))

m=Map(10,10)

g=game(actCtr,m)
for i in range(10):
    res=g.actorCtr.getAction()
    print(res)
    if res["action"]=="player":
        #put some code!
        pass
    if res["action"]=="move":
        actor=actCtr.actors[res["actId"]]
        target=actCtr.actors[res["targetId"]]
        if actor.x > target.x:
            actor.x-=1
        else:
            actor.x+=1
        if actor.y > target.y:
            actor.y -= 1
        else:
            actor.y+=1
