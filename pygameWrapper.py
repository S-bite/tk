# coding: utf-8
import pygame
import logging
import sys
import os
import Actor
import time
from world import cutWorldMapToDisplay
from variable import(
mapX,
mapY
)
from collections import deque
from pygame.locals import *
logging.basicConfig(level=logging.INFO)


pygame.font.init()




class pygameWrapper():
    def __init__(self, width=640, height=480, logMaxVisible=8, logMaxWidth=80, framerate=30, chipSize=32, fontSize=16):
        self.width, self.height = width, height + logMaxVisible * fontSize
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.screen = pygame.display.set_mode(self.rect.size)
        self.framerate = framerate
        self.FONT_SIZE = fontSize
        self.font = pygame.font.Font("meiryo.ttc", self.FONT_SIZE)
        self.logMessage = deque()
        self.LOG_MAX = self.height/self.FONT_SIZE
        self.LOG_MAX_VISIBLE = logMaxVisible
        self.LOG_MAX_WIDTH = logMaxWidth
        self.CHIP_SIZE = chipSize
        self.charList = self.getImageList("chars.bmp", transparent=True)
        self.fieldList = self.getImageList("chip12e_map_n.png", transparent=False)
        self.imageSources = [self.fieldList, self.charList]
        self.mapQueue=[]
        self.charQueue=[]
        self.itemQueue=[]
    def prepareRedraw(self):
        self.screen.fill((0, 0, 0))


    def appendLog(self, msg):
        # msg[i*max:(i+1)*max]で、msgをmax文字ごとに切り分ける
        lines = [msg[i * self.LOG_MAX_WIDTH:(i + 1) * self.LOG_MAX_WIDTH] for i in
             range(len(msg) // (self.LOG_MAX_WIDTH + 1) + 1)]
        for line in lines:
            if len(self.logMessage) >= self.LOG_MAX:
                self.logMessage.pop()
            self.logMessage.appendleft(line)
        self.update()
    def drawLog(self):
        i = 1
        for msg in self.logMessage:
            text = self.font.render(msg, False, (255, 255, 255))  # 描画する文字列の設定
            adjust=4 #そのままだと、最下層のメッセージが欠けるので、これを入れて調整する
            self.screen.blit(text, [0, self.height - adjust - i * self.FONT_SIZE])  # 文字列の表示位置
            i += 1
            if i>self.LOG_MAX_VISIBLE:
                break

    def drawSurface(self, char, x, y, x32=True):
        if x32:
            self.screen.blit(char, (x * 32, y * 32))
        else:
            self.screen.blit(char, (x, y))
    def drawHP(self,actor):
        pass# hukannzenn
        len=(float(actor.HP)/actor.HP_MAX)*self.CHIP_SIZE
        pygame.draw.line(self.screen, (255, 0, 0), (actor.x*self.CHIP_SIZE,actor.y*self.CHIP_SIZE),(actor.x*self.CHIP_SIZE\
                                                                                                    +len,actor.y*self.CHIP_SIZE),2)

    def drawImage(self, id, x, y, source, x32=True):
        self.drawSurface(self.imageSources[self.getImageIndex(source)][id], x, y, x32)

    def getImageIndex(self, source):
        if source == "field":
            index = 0
        elif source == "char":
            index = 1
        else:

            logging.error("Unknown Source : " + source)
            raise UnboundLocalError
        return index

    def drawMap(self, map, source):
        index = self.getImageIndex(source)
        for x in range(int(mapX)):
            for y in range(int(mapY)):

                if map[y][x] != -1:
                    self.drawSurface(self.imageSources[index][map[y][x]], x, y)

    def getImageList(self, filename, transparent=False):
        image = self.loadImage(filename, -1)
        imageList = []
        for x in range(0, image.get_width(), self.CHIP_SIZE):
            for y in range(0, image.get_height(), self.CHIP_SIZE):
                surface = pygame.Surface((self.CHIP_SIZE, self.CHIP_SIZE))
                surface.blit(image, (0, 0), (x, y, self.CHIP_SIZE, self.CHIP_SIZE))
                if transparent:
                    surface.set_colorkey(surface.get_at((0, 0)), RLEACCEL)
                surface.convert()
                imageList.append(surface)
        return imageList
    def draw(self,logOnly=False):
        self.drawMap(self.mapQueue,"map")
        self.drawMap(self.charQueue, "char")
        pass

    def update(self):

        self.screen.fill((0, 0, 0), pygame.Rect(0, self.height-(self.FONT_SIZE*self.LOG_MAX_VISIBLE), self.width, self.height))
        self.drawLog()
        pygame.display.update()

    def loadImage(self, filename, colorKey):
        filename = os.path.join("graphics", filename)
        try:
            image = pygame.image.load(filename)

        except pygame.error as message:
            logging.error("Can't load a image")
            raise pygame.error(message)
        image = image.convert()
        return image

stage=pygameWrapper(logMaxVisible=4)
