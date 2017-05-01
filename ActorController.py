#coding:utf-8

import numpy as np
from pygameWrapper import (
stage,
)
from variable import (
WAIT,
WAIT_KEY,
worldMap,
mapX,
mapY,
char,
)
from world import (
cutWorldMapToDisplay,
)
from Actor import (
actors,
)
import pygame

class ActorController():
    def __init__(self):
        pass
    def action(self):
        p=-1
        actors.sort(key=lambda actor: actor.SPD)
        for actor in actors:
            if actor.name=="Player":
                p=actor
                break
        if p==-1:
            print "Player not found"
        for actor in actors:
            if actor.act_state==WAIT_KEY:
                stage.drawMap(cutWorldMapToDisplay(worldMap, actor.x, actor.y, mapX, mapY), source="field")
                stage.drawMap(cutWorldMapToDisplay(char, actor.x, actor.y, mapX, mapY), "char")
                stage.update()
                while True:
                    pygame.time.wait(80)
                    res=pygame.event.get()
                    #pygame.key.set_repeat(300)
#                    pygame.event.clear()
                    pressedKeys = pygame.key.get_pressed()
                    pressedMods  = pygame.key.get_mods()
                    if np.sum(pressedKeys)>bin(pressedMods).count("1"):

                        print np.sum(pressedKeys),res
                        break
                actor.action(pressedKeys)
                stage.update()
            if actor.act_state==WAIT:
                actor.action(p)




