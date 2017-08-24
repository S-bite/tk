#coding:utf-8

from collections import deque
from Actor import Actor
from Actor import Enemy
from Actor import Player

import random as rnd
class ActorController():

    def __init__(self):
        self.actors={}
        self.move_queue=deque()
        self.player=None
        self.time=1

    def update_target(self,target):
        for _,actor in self.actors.items():
            if actor!=target:
                actor.target=target

    def set_actor_as_player(self,player):
        if player not in self.actors:
            assert ("argument is not in self.actors")
        self.player=player
    def del_actor_as_player(self,player):
        if player not in self.actors:
            assert("argument is not in self.actors")
        for _,actor in self.actors.items():
            if hasattr(actor,"target"):
                if actor.target==player:
                    actor.target=None

        self.player=None
        del_id=player.act_id
        self.actors.pop(del_id)

    def add_actor(self,actor,target=None):
        l=[i for i in self.actors]
        new_id=-1
        for n in range(len(l)+1):
            if n not in l:
                new_id=n
                break
        actor.target= target
        actor.act_id = new_id
        self.actors.update({new_id: actor})
    def add_actor_as_player(self,actor):
        self.add_actor(actor)
        self.set_actor_as_player(actor)

    def del_actor(self,del_target): #act_id or Actor どちらでも可
        del_id=None
        if type(del_target)==int:
            del_id=del_target
        elif type(del_target)==Actor or Enemy or Player:
            del_id=del_target.act_id
        self.actors.pop(del_id)

    def tick_for_move_queue(self):
        #print(self.move_queue)
        if self.move_queue:
            return 0
        id_list=[[x.act_id,x.SPD] for _,x in self.actors.items()]
        movables = []
        #print(id_list)
        while True:
            for actor in id_list:
                if self.time%(1023//actor[1])==0 and actor not in movables:
                    movables.append(actor)
            if len(movables)==0:
                self.time=max((self.time+1)%1024,1)
                continue
            else:
                movables.sort(reverse=True,key=lambda x:x[1])
                self.move_queue+=[self.actors[x[0]]for x in movables]
                break
        self.time = max((self.time + 1) % 1024, 1)
        return 0

    def get_next_actor(self):
        self.tick_for_move_queue()
        return self.move_queue[0]
    def get_action(self):
        self.tick_for_move_queue()
        print(self.move_queue)
        actor=self.move_queue.popleft()
        print(actor.name)
        res={"act_id":actor.act_id}
        res.update(actor.get_action())

        return res


def get_random_param():
    return {"HP":1,"x":20,"y":2,"job":"test","SPD":rnd.randint(30,60)}
if __name__=="__main__":
    actCtr=ActorController()
    p=Player({"SPD":15,"x":1,"y":2})
    actCtr.add_actor_as_player(p)
    actCtr.add_actor(Enemy({"SPD":20,"x":2,"y":2}),target=actCtr.player)
    print([x.SPD for _,x in actCtr.actors.items()])
    for i in range(100):
        request=actCtr.get_action()
        print(request)
