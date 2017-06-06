#coding:utf-8

from ActorController import ActorController
from Actor import Player,Enemy,Actor
from map import Map
class game():
    def __init__(self,actorCtr,fieldMap):
        self.actorCtr=actorCtr
        self.fieldMap=fieldMap


actCtr=ActorController()
p=Player({"name":"Player","SPD":9,"HP":10,"STR":5,"DEF":5,"x":5,"y":5})
actCtr.addActor(p)
actCtr.setActorAsPlayer(p)
actCtr.addActor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":9,"y":9,"dist":1}),target=actCtr.player)

m=Map(10,10)

g=game(actCtr,m)
for i in range(100):
    res=g.actorCtr.getAction()
    print(res)
    if res["action"]=="player":
        player=actCtr.actors[res["actId"]]
        cmd=input("action:").split(" ")
        if cmd[0]=="m":
            dir=cmd[1]
            if dir=="u":
                player.y-=1
            elif dir=="d":
                player.y+=1
            elif dir=="r":
                player.x-=1
            elif dir=="l":
                player.x+=1


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
    elif res["action"]=="attack":
        actor=actCtr.actors[res["actId"]]
        target=actCtr.actors[res["targetId"]]
        target.HP-=actor.STR//target.DEF
        print(actor.name,"attacks",target.name,"\b. ",target.name,"\b's HP is",target.HP)
        if target.HP < 0:
            if target in actCtr.moveQueue:
                actCtr.moveQueue.remove(target)
            if target==actCtr.player:
                actCtr.delActorAsPlayer(target)
            else:
                actCtr.delActor(target)
    for _,actor in actCtr.actors.items():
        print(actor.name,actor.x,actor.y,actor.HP)