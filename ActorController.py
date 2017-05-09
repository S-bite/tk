#coding:utf-8
from variable import (
WAIT,
WAIT_KEY,
worldMap,
mapX,
mapY,
char,
)
import numpy as np
from pygame.locals import *
import sys
from pygameWrapper import (
stage,
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
        def isOpenWindow(key):
            targetKeys = [K_z, K_c, K_v]
            for targetKey in targetKeys:
                print(pygame.key.name(targetKey),key[targetKey])
                if key[targetKey]:
                    return True
            return False
        def getKey():
            while True:
                pygame.time.wait(80)
                res = pygame.event.get()
                for event in res:
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        # pygame.key.set_repeat(300)
                        #                    pygame.event.clear()
                pressedKeys = pygame.key.get_pressed()
                pressedMods = pygame.key.get_mods()
                if np.sum(pressedKeys) > bin(pressedMods).count("1"):
                    break
            return pressedKeys
        p=-1
        actors.sort(key=lambda actor: actor.SPD)
        for actor in actors:
            if actor.name=="Player":
                p=actor
                break
        assert p != -1, "Player not found"
        for actor in actors:
            if actor.act_state==WAIT_KEY:# if actor is player
                #stage.drawChips(cutWorldMapToDisplay(worldMap, actor.x, actor.y, mapX, mapY), source="field")
                #stage.drawChips(cutWorldMapToDisplay(char, actor.x, actor.y, mapX, mapY), "char")
                #stage.update()
                while True:
                    pressedKeys=getKey()
                    if isOpenWindow(pressedKeys):
                        isActFinish=True # doSomething
                        if isActFinish:
                            break
                    else:
                        isActFinish = actor.action(pressedKeys)
                        if isActFinish:
                            break

                stage.update()
            if actor.act_state==WAIT:
                actor.action(p)
        stage.draw()
        for actor in actors:
            if actor!=p:
                stage.drawHP(actor, p)
        pygame.display.update()


