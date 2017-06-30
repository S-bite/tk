from Actor import Actor
import random


class field():
    def __init__(self, x=10, y=10,name="field",terrainData=None):
        def generateList(x, y, default):
            if type(default) != type(object):
                return [[default for _ in range(x)] for __ in range(y)]

            return [[default() for _ in range(x)] for __ in range(y)]

        self.terrain = generateList(x, y, 0)
        self.actor = generateList(x, y, None)
        self.item = generateList(x, y, None)
        self.door = generateList(x, y, None)
        self.rooms = []
        self.name=name
        self.height=y
        self.width=x
    def createRoom(self, sx, sy, sizex, sizey):
        isConflict = False
        tmp = self.terrain
        sizex, sizey = sizex + 1, sizey + 1
        for i in range(sizex + 1):
            if self.terrain[sy][sx + i] == 1 or self.terrain[sy + sizey][sx + i] == 1:
                isConflict = True
                break
            self.terrain[sy][sx + i] = 1
            self.terrain[sy + sizey][sx + i] = 1

        if isConflict:
            self.terrain = tmp
            return -1

        for i in range(1, sizey):
            if self.terrain[sy + i][sx] == 1 or self.terrain[sy + i][sx + sizex] == 1:
                isConflict = True
                break
            self.terrain[sy + i][sx] = 1
            self.terrain[sy + i][sx + sizex] = 1

        if isConflict:
            self.terrain = tmp
            return -1

        self.rooms.append((len(self.rooms), sx, sy, sizex, sizey))
        return 0

    def createBoarder(self):
        self.createRoom(0, 0, self.width - 2, self.height - 2)

    def setActor(self, actor):
        self.actor[actor.y][actor.x] = actor

    def delActor(self, actor):
        self.actor[actor.y][actor.x] = None

    def moveActor(self, actor, y, x):
        self.actor[actor.y][actor.x] = None
        self.actor[y][x] = actor

    def isMovable(self, x, y):
        if self.terrain[y][x] == 1:
            return False
        elif self.actor[y][x] != None:
            return False
        return True
    def getChipInfo(self,x,y):
        return {"actor":self.actor[y][x],"isMovable":self.isMovable(x,y),"item":self.item[y][x],"door":self.door[y][x]}
if __name__=="__main__":
    x = 500
    y = 500
    f = field(x, y)
    f.createBoarder()

    roomNum = 3
    cnt = 0
    while True:
        sizex = 0  # random.randint(10,200)
        sizey = 0  # random.randint(10,200)
        sx = random.randint(0, x - 1 - sizex)
        sy = random.randint(0, y - 1 - sizey)
        # print(sx,sy,sizex,sizey)
        res = f.createRoom(sx, sy, sizex, sizey)
        if res == 0:
            cnt += 1
            if cnt == roomNum:
                break
    print(f.isMovable(30, 10))