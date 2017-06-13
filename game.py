#coding:utf-8

from ActorController import ActorController
from Actor import Player,Enemy,Actor
from map import Map
class game():
    def __init__(self,fieldIndex=[],currentIndex=0):
        self.fieldIndex=[]
        for index in fieldIndex:
            self.fieldIndex.append([index[0].name,index[0],index[1]])
        self.actorCtr=fieldIndex[currentIndex][1]
        self.fieldMap=fieldIndex[currentIndex][0]
        for _,actor in self.actorCtr.actors.items():
            self.fieldMap.setActor(actor)
    def exeAct(self,action,actorId,targetId):
        actor=self.actorCtr.actors[actorId]
        target=self.actorCtr.actors[targetId]
        print("action",action)
        if action == "player":
            player=actor
            while True:
                cmd = input("action:").split(" ")
                if cmd[0] == "m":
                    mx=0
                    my=0
                    dir = cmd[1]
                    if "u" in dir:
                        my -= 1
                    if "d" in dir:
                        my += 1
                    if "r" in dir:
                        mx += 1
                    if "l" in dir:
                        mx -= 1
                    if self.fieldMap.map[player.y+my][player.x+mx].isMovable==True:
                        self.fieldMap.moveActor(player,player.y+my,player.x+mx)
                        player.x+=mx
                        player.y+=my
                        break
                    else:
                        print("you can't move there")
                if cmd[0]=="l":
                    for _,a in g.actorCtr.actors.items():
                        print(a.actId,a.name,a.x,a.y,a.HP)
                if cmd[0]=="M":
                    for y in range(self.fieldMap.height):
                        s=""
                        for x in range(self.fieldMap.width):
                            p=self.fieldMap.map[y][x]
                            a=p.actor
                            if a!=None:
                                s+=a.name[0]
                            elif p.dest!=None:
                                s+="/"
                            else :
                                if p.isMovable:
                                    s+="."
                                else:
                                    s+="#"
                        print (s)
                if cmd[0]=="t":
                    player.target=self.actorCtr.actors[int(cmd[1])]
                if cmd[0]=="w":

                    self.fieldMap.moveActor(player, int(cmd[2]), int(cmd[1]))
                    player.x=int(cmd[1])
                    player.y=int(cmd[2])
                    break
                if cmd[0]=="n":
                    break
                if cmd[0]=="s":
                    print(player.name,player.HP,player.STR,player.DEF)
                if cmd[0]=="f":
                    if player.target==None:
                        print("target is not selected")
                    else:
                        dist=abs(player.target.x-player.x)+abs(player.target.y-player.y)
                        player.target.HP-=int((player.STR//target.DEF)*3*(0.8**dist))
                        print(player.target.HP)
                        if player.target.HP < 0:
                            self.fieldMap.delActor(player.target)
                            if player.target in self.actorCtr.moveQueue:
                                self.actorCtr.moveQueue.remove(player.target)
                            if player.target == self.actorCtr.player:
                                self.actorCtr.delActorAsPlayer(player.target)
                            else:
                                self.actorCtr.delActor(player.target)
                            player.target = None
                        break
                if cmd[0]=="g":
                    p=self.fieldMap.map[self.actorCtr.player.y][self.actorCtr.player.y]
                    if p.dest!=None:
                        _p=self.actorCtr.player
                        print("move",p.dest[0])
                        index=None
                        print(self.fieldIndex)
                        for _index in self.fieldIndex:
                            if _index[0]==p.dest[0]:
                                index=_index
                        if index==None:
                            Exception("index not found")
                        print(index)
                        self.actorCtr=index[2]
                        self.fieldMap=index[1]
                        #player != actors
                        self.actorCtr.player=_p
                        self.actorCtr.actors[self.actorCtr.player.actId]=_p
                        self.actorCtr.player.x=int(p.dest[1])
                        self.actorCtr.player.y=int(p.dest[2])
                        self.actorCtr.updateTarget(_p)

                        for _, actor in self.actorCtr.actors.items():
                            self.fieldMap.setActor(actor)
                        break
                    else:
                        print("no port found")

                if cmd[0]=="q":
                    exit(0)
        elif action == "move":
            dist = abs(actor.x - target.x) + abs(actor.y - target.y)
            print("actor.x:", actor.x, "target.x", target.x, "dist:", dist)
            mx=0
            my=0
            if dist > actor.dist:
                if actor.x > target.x:
                    mx -= 1
                else:
                    mx += 1
                dist = abs(actor.x - target.x) + abs(actor.y - target.y)
                if dist > actor.dist:
                    if actor.y > target.y:
                        my -= 1
                    else:
                        my += 1
            elif dist < actor.dist:
                if actor.x > target.x:
                    mx += 1
                else:
                    mx -= 1
                dist = abs(actor.x - target.x) + abs(actor.y - target.y)
                if dist < actor.dist:
                    if actor.y > target.y:
                        my += 1
                    else:
                        my -= 1
            if self.fieldMap.map[actor.y+my][actor.x+mx].isMovable==True:
                self.fieldMap.moveActor(actor,actor.y+my,actor.x+mx)
                actor.x+=mx
                actor.y+=my
        elif action == "attack":
            if abs(target.x - actor.x) <= 1 and abs(target.y - actor.y) <= 1:
                target.HP -= actor.STR // target.DEF
                print(actor.name, "attacks", target.name, "\b. ", target.name, "\b's HP is", target.HP)
                if target.HP < 0:
                    self.fieldMap.delActor(target)
                    if target in g.actorCtr.moveQueue:
                        g.actorCtr.moveQueue.remove(target)
                    if target == g.actorCtr.player:
                        g.actorCtr.delActorAsPlayer(target)
                    else:
                        g.actorCtr.delActor(target)
            else:
                print(actor.name, "attacks but too far.")





room1Act=ActorController()
p=Player({"name":"Player","SPD":20,"HP":10,"STR":15,"DEF":5,"x":5,"y":5})
room1Act.addActor(p)
room1Act.setActorAsPlayer(p)
room1Act.addActor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":9,"y":9,"dist":1}),target=room1Act.player)
room1Act.addActor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":3,"y":4,"dist":1}),target=room1Act.player)
l=[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

]
room1Map=Map("room1",mapData=l)
room1Map.map[1][1].dest=["room2",8,8]


room2Act=ActorController()
p=Player({"name":"Player","SPD":20,"HP":10,"STR":15,"DEF":5,"x":5,"y":5})
room2Act.addActor(p)
room2Act.setActorAsPlayer(p)
room2Act.addActor(Enemy({"name":"bat","SPD":10,"HP":5,"STR":10,"DEF":8,"x":1,"y":1,"dist":1}),target=room2Act.player)
room2Act.addActor(Enemy({"name":"bat","SPD":10,"HP":5,"STR":10,"DEF":8,"x":8,"y":1,"dist":1}),target=room2Act.player)
l=[
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],

]
room2Map=Map("room2",mapData=l)
room2Map.map[8][8].dest=["room1",1,1]

g=game([(room1Map,room1Act),(room2Map,room2Act)],1)

for i in range(100):
    res=g.actorCtr.getAction()
    g.exeAct(res["action"],res["actId"],res["targetId"])
    for _,actor in g.actorCtr.actors.items():
        print(actor.name,actor.x,actor.y,actor.HP)