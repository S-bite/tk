#coding:utf-8

from ActorController import ActorController
from Actor import Player,Enemy,Actor
from field import field
from input import key
import enum
import pyglet.window.key

class screenStateEnum(enum.IntEnum):
    ON_MAP=0
    ON_CHAT=1
    ON_INVENTORY=2
class mapHandler():
    pass
class inventoryHandler():
    pass
class chatHandler():
    pass

class game():
    def __init__(self,stageDatas,currentStage=0):
        self.stageDatas=[]
        for stageData in stageDatas:
            self.stageDatas.append([stageData["field"].name,stageData["field"],stageData["ActorController"]])
        self.actorCtr=stageDatas[currentStage]["ActorController"]
        self.fieldMap=stageDatas[currentStage]["field"]
        self.screen_state=screenStateEnum.ON_MAP
        for _,actor in self.actorCtr.actors.items():
            self.fieldMap.setActor(actor)

    def step(self,keys):
        res=self.actorCtr.get_action()
        print(res)
        self.exe_act(res["action"],res["act_id"],res["target_id"])

        if self.screen_state==screenStateEnum.ON_MAP:
            print("ON_MAP")
        if "UP" in keys:
            #movehandler.up()

            print("UP")

        return 0

    def exe_act(self,action,actor_id,target_id):
        def kill_actor(actor,target):
            self.fieldMap.delActor(target)
            if target in self.actorCtr.move_queue:
                self.actorCtr.move_queue.remove(target)
            if target == self.actorCtr.player:
                self.actorCtr.del_actor_as_player(target)
            else:
                self.actorCtr.del_actor(target)
            actor.target = None
        def attack(actor,target):
            target.HP -= int((actor.STR // target.DEF) * 3)
            print(actor.name,"attacks",target.name)
            if target.HP < 0:
                kill_actor(actor, target)
        def show_map():
            for y in range(self.fieldMap.height):
                s = ""
                for x in range(self.fieldMap.width):
                    p = self.fieldMap.getChipInfo(x,y)
                    a=p["actor"]
                    if a != None:
                        s += a.name[0]
                    elif p["door"] != None:
                        s += "/"
                    else:
                        if p["isMovable"]:
                            s += "."
                        else:
                            s += "#"
                print(s)

        print("\x1b[2J\x1b[H")
        show_map()
        #print(msg) or something like that!
        actor=self.actorCtr.actors[actor_id]
        target=self.actorCtr.actors[target_id]
        print("action",action)
        if action == "player":
            player=actor

            while True:
                #pushed=keyBoard.getInput()
                #if len(pushed)==1:
                #    cmd = [pushed[0]]
                #else:
                #    if pushed[0]=="\x1b":
                #        cmd=["m",pushed[2]]
                cmd=input()
                if cmd[0] == "m":
                    mx=0
                    my=0
                    dir = cmd[1]
                    if "A" in dir: #up
                        my -= 1
                    if "B" in dir:#down
                        my += 1
                    if "C" in dir:#right
                        mx += 1
                    if "D" in dir:#left
                        mx -= 1
                    if self.fieldMap.isMovable(player.x+mx,player.y+my)==True:
                        self.fieldMap.moveActor(player,player.y+my,player.x+mx)
                        player.x+=mx
                        player.y+=my
                        break
                    elif self.fieldMap.actor[player.y+my][player.x+mx]!=None:
                        target=self.fieldMap.actor[player.y+my][player.x+mx]
                        attack(player,target)
                    else:
                        print("you can't move there")
                if cmd[0]=="l":
                    for _,a in self.actorCtr.actors.items():
                        print(a.act_id,a.name,a.x,a.y,a.HP)
                if cmd[0]=="M":
                    show_map()
                if cmd[0]=="t":
                    print("select target")
                    t=int(input())#keyBoard.getInput()[0])

                    player.target=self.actorCtr.actors[t]
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
                            kill_actor(player,player.target)
                        break
                if cmd[0]=="g":
                    p=self.fieldMap.getChipInfo(self.actorCtr.player.x,self.actorCtr.player.y)
                    if p["door"] is not None:
                        _p=self.actorCtr.player
                        index=None
                        print(self.stageDatas)
                        for stageData in self.stageDatas:
                            if stageData[0]==p["door"][0]:
                                index=stageData
                        if index is None:
                            raise Exception("index not found")
                        print(type(index))
                        self.actorCtr=index[2]
                        self.fieldMap=index[1]
                        self.actorCtr.player=_p
                        self.actorCtr.actors[self.actorCtr.player.act_id]=_p
                        self.actorCtr.player.x=int(p["door"][1])
                        self.actorCtr.player.y=int(p["door"][2])
                        self.actorCtr.update_target(_p)

                        for _, actor in self.actorCtr.actors.items():
                            self.fieldMap.setActor(actor)
                        break
                    else:
                        print("no port found")

                if cmd[0]=="q":
                    print("\x1b[2J\x1b[H")
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
            if self.fieldMap.isMovable(actor.x+mx,actor.y+my)==True:
                self.fieldMap.moveActor(actor,actor.y+my,actor.x+mx)
                actor.x+=mx
                actor.y+=my
        elif action == "attack":
            if abs(target.x - actor.x) <= 1 and abs(target.y - actor.y) <= 1:
                target.HP -= actor.STR // target.DEF
                print(actor.name, "attacks", target.name, "\b. ", target.name, "\b's HP is", target.HP)
                if target.HP < 0:
                    self.fieldMap.delActor(target)
                    if target in g.actorCtr.move_queue:
                        g.actorCtr.move_queue.remove(target)
                    if target == g.actorCtr.player:
                        g.actorCtr.del_actor_as_player(target)
                    else:
                        g.actorCtr.del_actor(target)
            else:
                print(actor.name, "attacked but too far.")


if __name__=="__main__":
    room1_act=ActorController()
    p=Player({"name":"Player","SPD":20,"HP":100,"STR":150,"DEF":5,"x":5,"y":5})
    room1_act.add_actor_as_player(p)
    room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":8,"y":1,"dist":1}),target=room1_act.player)
    room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":3,"y":4,"dist":1}),target=room1_act.player)
    room1_map=field(name="room1")
    room1_map.door[1][1]=["room2",8,8]

    room2_act=ActorController()
    p=Player({"name":"Player","SPD":20,"HP":100,"STR":150,"DEF":5,"x":5,"y":5})
    room2_act.add_actor_as_player(p)
    room2_act.add_actor(Enemy({"name":"bat","SPD":10,"HP":5,"STR":10,"DEF":8,"x":1,"y":1,"dist":1}),target=room2_act.player)
    room2_act.add_actor(Enemy({"name":"bat","SPD":10,"HP":5,"STR":10,"DEF":8,"x":8,"y":1,"dist":1}),target=room2_act.player)

    room2_map=field(name="room2")
    room2_map.createBoarder()
    room2_map.door[8][8]=["room1",1,1]

    g=game([{"field":room1_map,"ActorController":room1_act},{"field":room2_map,"ActorController":room2_act}],1)

    while True:
        g.exe_act()