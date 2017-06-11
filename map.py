import numpy as np
class Map():
    def __init__(self,name,height=1,width=1,mapData=None):
        class Chip():
            def __init__(self, isMovable=True, type="GLASS"):
                self.isMovable = isMovable
                self.type = type
                self.dest=None
                self.actor=None

        self.name = ""
        if mapData==None:
            self.height = height
            self.width = width
            self.map=[[Chip() for _ in range(self.width)]for __ in range(self.height)]
        else:
            mapData=np.array(mapData)
            if len(mapData.shape)!=2:
                Exception("invalid mapList shape")
            self.height = mapData.shape[0]
            self.width = mapData.shape[1]
            self.map=[[Chip(isMovable=[True,False][mapData[y][x]]) for x in range(self.width)] for y in range(self.height)]
    def setActor(self,actor):
        self.map[actor.y][actor.x].actor = actor
    def delActor(self,actor):
        self.map[actor.y][actor.x].actor = None
    def moveActor(self,actor,y,x):
        self.map[actor.y][actor.x].actor=None
        self.map[y][x].actor=actor
if __name__=="__main__":
    m=Map(20,10)

