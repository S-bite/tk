

#needless?
import numpy as np
class Map():
    MAP_TYPE={
        "GLASS":0,
        "SEA":1,
    }
    MAP_MOVABLE=[MAP_TYPE["GLASS"]]

    def __init__(self,height,width):
        self.map=np.zeros((height,width))
    def setType(self,y,x,type):
        self.map[y][x]=self.MAP_TYPE[type]
    def isMovable(self,y,x):
        if self.map[y][x] in self.MAP_MOVABLE:
            return True
        return False


if __name__=="__main__":
    m=Map(20,20)
    m.setType(10,12,"SEA")
    print(m.isMovable(1,12))

