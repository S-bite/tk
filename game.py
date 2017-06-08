#coding:utf-8

from ActorController import ActorController
from Actor import Player,Enemy,Actor
from map import Map
class game():

    def __init__(self,actorCtr,fieldMap):
        self.actorCtr=actorCtr
        self.fieldMap=fieldMap

    def excAct(self,action,actorId,targetId):
        actor=self.actorCtr.actors[actorId]
        target=self.actorCtr.actors[targetId]
        print("action",action)
        if action == "player":
            player=actor
            while True:
                cmd = input("action:").split(" ")
                if cmd[0] == "m":
                    dir = cmd[1]
                    if "u" in dir:
                        player.y -= 1
                    if "d" in dir:
                        player.y += 1
                    if "r" in dir:
                        player.x -= 1
                    if "l" in dir:
                        player.x += 1
                    break
                if cmd[0]=="l":
                    for _,a in g.actorCtr.actors.items():
                        print(a.actId,a.name)

                if cmd[0]=="t":
                    player.target=self.actorCtr.actors[int(cmd[1])]

                if cmd[0]=="s":
                    print(player.name,player.HP,player.STR,player.DEF)
        elif action == "move":
            dist = abs(actor.x - target.x) + abs(actor.y - target.y)
            print("actor.x:", actor.x, "target.x", target.x, "dist:", dist)
            if dist > actor.dist:
                if actor.x > target.x:
                    actor.x -= 1
                else:
                    actor.x += 1
                dist = abs(actor.x - target.x) + abs(actor.y - target.y)
                if dist > actor.dist:
                    if actor.y > target.y:
                        actor.y -= 1
                    else:
                        actor.y += 1
            elif dist < actor.dist:
                if actor.x > target.x:
                    actor.x += 1
                else:
                    actor.x -= 1
                dist = abs(actor.x - target.x) + abs(actor.y - target.y)
                if dist < actor.dist:
                    if actor.y > target.y:
                        actor.y += 1
                    else:
                        actor.y -= 1
        elif action == "attack":
            if abs(target.x - actor.x) <= 1 and abs(target.y - actor.y) <= 1:
                target.HP -= actor.STR // target.DEF
                print(actor.name, "attacks", target.name, "\b. ", target.name, "\b's HP is", target.HP)
                if target.HP < 0:
                    if target in actCtr.moveQueue:
                        g.actorCtr.moveQueue.remove(target)
                    if target == actCtr.player:
                        g.actorCtr.delActorAsPlayer(target)
                    else:
                        g.actorCtr.delActor(target)
            else:
                print(actor.name, "attacks but too far.")





actCtr=ActorController()
p=Player({"name":"Player","SPD":9,"HP":1,"STR":5,"DEF":5,"x":5,"y":5})
actCtr.addActor(p)
actCtr.setActorAsPlayer(p)
actCtr.addActor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":9,"y":9,"dist":1}),target=actCtr.player)

m=Map(10,10)

g=game(actCtr,m)
for i in range(100):
    res=g.actorCtr.getAction()
    g.excAct(res["action"],res["actId"],res["targetId"])
    for _,actor in actCtr.actors.items():
        print(actor.name,actor.x,actor.y,actor.HP)