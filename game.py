#coding:utf-8

from ActorController import ActorController
from Actor import Player,Enemy,Actor
from field import field
from input import key
import random
import enum
import pyglet.window.key
from collections import deque
class screenStateEnum(enum.IntEnum):
    ON_MAP=0
    ON_CHAT=1
    ON_INVENTORY=2

class game():
    def __init__(self,stage_datas,current_stage=0):
        self.game_log=deque()
        self.stage_datas=[]
        for stage_data in stage_datas:
            self.stage_datas.append([stage_data["field"].name,stage_data["field"],stage_data["ActorController"]])
        self.actor_ctr=stage_datas[current_stage]["ActorController"]
        self.field_map=stage_datas[current_stage]["field"]
        self.screen_state=screenStateEnum.ON_MAP
        for _,actor in self.actor_ctr.actors.items():
            self.field_map.set_actor(actor)
        print(self.actor_ctr.player)

    def operate_game_on_map_state(self,keys):
        #define some macro here
        def kill_actor(actor, target):
            self.field_map.del_actor(target)
            if target in self.actor_ctr.move_queue:
                self.actor_ctr.move_queue.remove(target)
            if target == self.actor_ctr.player:
                self.actor_ctr.del_actor_as_player(target)
            else:
                self.actor_ctr.del_actor(target)
            self.game_log.append(actor.name + " killed " + target.name)

            actor.target = None

        def attack_actor(actor, target):
            target.HP -= int((actor.STR // target.DEF) * 3)
            self.game_log.append(actor.name+" attacks "+target.name)
            if target.HP < 0:
                kill_actor(actor, target)
        def is_contain(keys,subs):
            for sub in subs:
                if not sub in keys:
                    break
            else:
                return True
            return False

        #macro ends



        actor=self.actor_ctr.get_next_actor()

        #if actor is not player
        if not actor.is_player:


            actor = self.actor_ctr.pick_next_actor()
            #単なる距離ではなく、移動（斜め含む）でたどり着ける最短手数
            move_distance=-1 if actor.target==None else (abs(actor.x-actor.target.x),abs(actor.y-actor.target.y))
            if move_distance==1:
                attack_actor(actor,actor.target)
                return -1
            action=actor.get_action()
            if action["action"]=="move_random":
                mx=random.randint(-1,1)
                my = random.randint(-1, 1)
                if self.field_map.is_movable(actor.x+mx,actor.y+my):
                    self.field_map.move_actor(actor,actor.x+mx,actor.y+my)
                    actor.x += mx
                    actor.y += my

                    return -1
            elif action["action"]=="move":
                mx = (actor.target.x-actor.x)//max(abs(actor.target.x-actor.x),1)
                my = (actor.target.y-actor.y)//max(abs(actor.target.y-actor.y),1)
                if self.field_map.is_movable(actor.x + mx, actor.y + my):
                    self.field_map.move_actor(actor, actor.x + mx, actor.y + my)
                    actor.x += mx
                    actor.y += my

                return -1

            return -1
        else:

            if keys==[]:
                return 1
            actor = self.actor_ctr.pick_next_actor()

            mx, my = 0, 0
            if "UP" in keys:  # up
                my -= 1
            if "DOWN" in keys:  # down
                my += 1
            if "RIGHT" in keys:  # right
                mx += 1
            if "LEFT" in keys:  # left
                mx -= 1
            #方向キーのいずれかが押されていたら
            if mx !=0 or my!=0:
                if self.field_map.is_movable(actor.x + mx, actor.y + my):
                    self.field_map.move_actor(actor, actor.x + mx, actor.y + my)
                    actor.x += mx
                    actor.y += my
                elif self.field_map.is_occupied_by_actor(actor.x+mx,actor.y+my):
                    attack_actor(actor,self.field_map.get_actor(actor.x+mx,actor.y+my))



            return 1



    def step(self,keys):
        if self.screen_state==screenStateEnum.ON_MAP:
            while self.operate_game_on_map_state(keys)!=1:
                pass

        return self
    def exe_act(self,action,actor_id,target_id,pushed_key=None):
        cmd=pushed_key
        def kill_actor(actor,target):
            self.field_map.del_actor(target)
            if target in self.actor_ctr.move_queue:
                self.actor_ctr.move_queue.remove(target)
            if target == self.actor_ctr.player:
                self.actor_ctr.del_actor_as_player(target)
            else:
                self.actor_ctr.del_actor(target)
            print("killed!")
            actor.target = None

        def attack(actor,target):
            target.HP -= int((actor.STR // target.DEF) * 3)
            print(actor.name,"attacks",target.name)
            if target.HP < 0:
                kill_actor(actor, target)

        def show_map():
            pass
            for y in range(self.field_map.height):
                s = ""
                for x in range(self.field_map.width):
                    p = self.field_map.get_chip_info(x,y)
                    a=p["actor"]
                    if a != None:
                        s += a.name[0]
                    elif p["door"] != None:
                        s += "/"
                    else:
                        if p["is_movable"]:
                            s += "."
                        else:
                            s += "#"
                print(s)

        print("\x1b[2J\x1b[H")
        actor=self.actor_ctr.actors[actor_id]
        target=self.actor_ctr.actors[target_id]
        print("action",action)
        if action == "player":
            player=actor
            mx,my=0,0
            if "UP" in cmd: #up
                my -= 1
            if "DOWN" in cmd:#down
                my += 1
            if "RIGHT" in cmd:#right
                mx += 1
            if "LEFT" in cmd:#left
                mx -= 1
            if self.field_map.is_movable(player.x+mx,player.y+my)==True:
                self.field_map.move_actor(player,player.y+my,player.x+mx)
                player.x+=mx
                player.y+=my
            elif self.field_map.actor[player.y+my][player.x+mx]!=None:
                target=self.field_map.actor[player.y+my][player.x+mx]
                attack(player,target)
            else:
                print("you can't move there")
            print(self.actor_ctr.player,2344)
            if "L" in cmd:
                for _,a in self.actor_ctr.actors.items():
                    print(a.act_id,a.name,a.x,a.y,a.HP)
            if "M" in cmd:
                show_map()
            if "T"in cmd:
                print("select target")
                t=int(input())#keyBoard.getInput()[0])

                player.target=self.actor_ctr.actors[t]
            if cmd[0]=="w":
                self.field_map.move_actor(player, int(cmd[2]), int(cmd[1]))
                player.x=int(cmd[1])
                player.y=int(cmd[2])
            if cmd[0]=="n":
                pass
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
            if cmd[0]=="G":
                print(self.actor_ctr.player,123)
                p=self.field_map.get_chip_info(self.actor_ctr.player.x,self.actor_ctr.player.y)
                if p["door"] is not None:
                    _p=self.actor_ctr.player
                    index=None
                    print(self.stage_datas)
                    for stageData in self.stage_datas:
                        if stageData[0]==p["door"][0]:
                            index=stageData
                    if index is None:
                        raise Exception("index not found")
                    print(type(index))
                    self.actor_ctr=index[2]
                    self.field_map=index[1]
                    self.actor_ctr.player=_p
                    self.actor_ctr.actors[self.actor_ctr.player.act_id]=_p
                    self.actor_ctr.player.x=int(p["door"][1])
                    self.actor_ctr.player.y=int(p["door"][2])
                    self.actor_ctr.update_target(_p)
                    for _, actor in self.actor_ctr.actors.items():
                        self.field_map.set_actor(actor)
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
            if self.field_map.is_movable(actor.x+mx,actor.y+my)==True:
                self.field_map.move_actor(actor,actor.y+my,actor.x+mx)
                actor.x+=mx
                actor.y+=my
        elif action == "attack":
            if abs(target.x - actor.x) <= 1 and abs(target.y - actor.y) <= 1:
                target.HP -= actor.STR // target.DEF
                print(actor.name, "attacks", target.name, "\b. ", target.name, "\b's HP is", target.HP)
                if target.HP < 0:
                    self.field_map.delActor(target)
                    if target in g.actor_ctr.move_queue:
                        g.actor_ctr.move_queue.remove(target)
                    if target == g.actor_ctr.player:
                        g.actor_ctr.del_actor_as_player(target)
                    else:
                        g.actor_ctr.del_actor(target)
            else:
                print(actor.name, "attacked but too far.")
        show_map()
        print(self.actor_ctr.player)
        return self

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
    room2_map.create_boarder()
    room2_map.door[8][8]=["room1",1,1]

    g=game([{"field":room1_map,"ActorController":room1_act},{"field":room2_map,"ActorController":room2_act}],1)

    while True:
        g.exe_act()