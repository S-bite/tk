import random
mapX=640/32
mapY=480/32
char = [[-1 for i in xrange(256)] for j in xrange(256)]
actors=[]
NOACT=0
ACTED=1
WAIT_KEY=2
WAIT=3
LAND=5
SEA=3
idList=[0 for i in xrange(1024)]

worldMap=[[0 for i in xrange(256)] for j in xrange(256)]
for i in xrange(256*256):
    worldMap[random.randint(0,255)][random.randint(0,255)]=1



def worldInit(n):
    def func(x,y):
        s = worldMap[y + 1][x + 1] + worldMap[y + 1][x - 1] + worldMap[y + 1][x] + worldMap[y][x + 1] + worldMap[y][x - 1] + \
            worldMap[y - 1][x + 1] + worldMap[y - 1][x] + worldMap[y - 1][x - 1]
        if s == 0:
            worldMap[y][x] = 0
        elif s == 1:
            worldMap[y][x] = 1
            if random.randint(1, 100) < 100:
                worldMap[y][x] = 0
        elif s == 2:
            worldMap[y][x] = 1
            if random.randint(1, 100) < 100:
                worldMap[y][x] = 0
        elif s == 3:
            worldMap[y][x] = 1
            if random.randint(1, 100) < 100:
                worldMap[y][x] = 0
        elif s == 4:
            worldMap[y][x] = 1
            if random.randint(1, 100) < 50:
                worldMap[y][x] = 0
        elif s == 6:
            worldMap[y][x] = 1
            if random.randint(1, 100) < 10:
                worldMap[y][x] = 0
        elif s == 7:
            worldMap[y][x] = 1
            if random.randint(1, 100) < 0:
                worldMap[y][x] = 0
        elif s == 8:
            worldMap[y][x] = 1
    for x in xrange(256):
        for y in xrange(256):
            if worldMap[y][x]==LAND:
                worldMap[y][x]=0
            elif worldMap[y][x]==SEA:
                worldMap[y][x]=1

    for t in xrange(n):
        for i in xrange(256-2):
            for j in xrange(256-2):
                x,y=i+1,j+1
                func(x,y)

    for x in xrange(256):
        for y in xrange(256):
            if worldMap[y][x]==0:
                worldMap[y][x]=LAND
            else:
                worldMap[y][x]=SEA
