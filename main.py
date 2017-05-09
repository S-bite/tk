# coding:utf-8
import variable
from Actor import *
from ActorController import *
from world import *

l = stage.getImageList("chars.bmp")
clock = pygame.time.Clock()


class mapController():
    def __init__(self):
        self.field = []
        self.char = []
        self.item = []


currentMap = mapController()

accn = ActorController()


def main():
    worldInit(10)
    px = random.randint(0, 256)
    py = random.randint(0, 256)
    while not worldMap[py][px] == LAND:
        px = random.randint(0, 255)
        py = random.randint(0, 255)

    pData = [getNewId(), "Player", 96, "None", "Human", 100, 100, 50, 50, 10, ["Normal"]]
    pPos = [px, py]

    p = Player(pData, pPos)
    p.act_state = WAIT_KEY
    actors.append(p)
    for i in range(100):
        e = Enemy(
            [getNewId(), "ene", random.randint(1, 90), "None", "Gob", 100, 100, 50, 50, 5, ["Normal"]],
            [random.randint(0, 255), random.randint(0, 255)])
        e.act_state = WAIT
        actors.append(e)

    while True:
        stage.prepareRedraw()
        # print cutWorldMapToDisplay(worldMap, p.x,p.y,mapX,mapY)

        stage.mapQueue=cutWorldMapToDisplay(worldMap, p.x, p.y, mapX, mapY)
        stage.charQueue=cutWorldMapToDisplay(char, p.x, p.y, mapX, mapY)
        stage.draw()
        accn.action()
        #stage.drawChips(cutWorldMapToDisplay(worldMap, p.x, p.y, mapX, mapY), source="field")
        #stage.drawChips(cutWorldMapToDisplay(char, p.x, p.y, mapX, mapY), "char")
        clock.tick(60)
        #stage.draw()

if __name__ == '__main__':

    main()
