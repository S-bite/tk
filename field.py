from Actor import Actor
import random


class field():
    def __init__(self, x=10, y=10,name="field",terrain_data=None):
        def generate_list(x, y, default):
            if type(default) != type(object):
                return [[default for _ in range(x)] for __ in range(y)]

            return [[default() for _ in range(x)] for __ in range(y)]

        self.terrain = generate_list(x, y, 0)
        self.actor = generate_list(x, y, None)
        self.item = generate_list(x, y, None)
        self.door = generate_list(x, y, None)
        self.rooms = []
        self.name=name
        self.height=y
        self.width=x
    def create_room(self, sx, sy, sizex, sizey):
        is_conflict = False
        tmp = self.terrain
        sizex, sizey = sizex + 1, sizey + 1
        for i in range(sizex + 1):
            if self.terrain[sy][sx + i] == 1 or self.terrain[sy + sizey][sx + i] == 1:
                is_conflict = True
                break
            self.terrain[sy][sx + i] = 1
            self.terrain[sy + sizey][sx + i] = 1

        if is_conflict:
            self.terrain = tmp
            return -1

        for i in range(1, sizey):
            if self.terrain[sy + i][sx] == 1 or self.terrain[sy + i][sx + sizex] == 1:
                is_conflict = True
                break
            self.terrain[sy + i][sx] = 1
            self.terrain[sy + i][sx + sizex] = 1

        if is_conflict:
            self.terrain = tmp
            return -1

        self.rooms.append((len(self.rooms), sx, sy, sizex, sizey))
        return 0

    def create_boarder(self):
        self.create_room(0, 0, self.width - 2, self.height - 2)

    def set_actor(self, actor):
        self.actor[actor.y][actor.x] = actor

    def del_actor(self, actor):
        self.actor[actor.y][actor.x] = None

    def move_actor(self, actor, x, y):
        self.actor[actor.y][actor.x] = None
        self.actor[y][x] = actor

    def get_actor(self,x,y):
        return self.actor[y][x]
    def is_occupied_by_actor(self,x,y):
        if self.actor[y][x] != None:
            return True
        return False
    def is_movable(self, x, y):
        if self.terrain[y][x] == 1:
            return False
        elif self.actor[y][x] != None:
            return False
        return True
    def get_chip_info(self,x,y):
        return {"actor":self.actor[y][x],"is_movable":self.is_movable(x,y),"item":self.item[y][x],"door":self.door[y][x]}
if __name__=="__main__":
    x = 500
    y = 500
    f = field(x, y)
    f.create_boarder()

    room_num = 3
    cnt = 0
    while True:
        sizex = 0  # random.randint(10,200)
        sizey = 0  # random.randint(10,200)
        sx = random.randint(0, x - 1 - sizex)
        sy = random.randint(0, y - 1 - sizey)
        # print(sx,sy,sizex,sizey)
        res = f.create_room(sx, sy, sizex, sizey)
        if res == 0:
            cnt += 1
            if cnt == room_num:
                break
    print(f.is_movable(30, 10))