import numpy as np
#NO USE#
class Map():
    def __init__(self,name,height=1,width=1,map_data=None):
        class Chip():
            def __init__(self, is_movable=True, type="GLASS"):
                self.is_movable = is_movable
                self.type = type
                self.dest=None
                self.actor=None

        self.name = name
        if map_data==None:
            self.height = height
            self.width = width
            self.map=[[Chip() for _ in range(self.width)]for __ in range(self.height)]
        else:
            map_data=np.array(map_data)
            if len(map_data.shape)!=2:
                Exception("invalid mapList shape")
            self.height = map_data.shape[0]
            self.width = map_data.shape[1]
            self.map=[[Chip(is_movable=[True,False][map_data[y][x]]) for x in range(self.width)] for y in range(self.height)]
    def set_actor(self,actor):
        self.map[actor.y][actor.x].actor = actor
        self.map[actor.y][actor.x].is_movable = False

    def del_actor(self,actor):
        self.map[actor.y][actor.x].actor = None
        self.map[actor.y][actor.x].is_movable = True

    def move_actor(self,actor,y,x):
        self.map[actor.y][actor.x].actor=None
        self.map[actor.y][actor.x].is_movable=True
        self.map[y][x].actor=actor
        raise Exception ("foo")
        self.map[y][x].is_movable = False
if __name__=="__main__":
    m=Map(20,10)

