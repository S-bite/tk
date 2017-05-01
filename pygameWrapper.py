# coding: utf-8
import pygame
import sys
import os
import time
from collections import deque
from pygame.locals import *
mapX=640/32
mapY=480/32

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

    def prepareRedraw(self):
        self.screen.fill((0, 0, 0))

    def appendLog(self, msg):
        # msg[i*max:(i+1)*max]で、msgをmax文字ごとに切り分ける
        l = [msg[i * self.LOG_MAX_WIDTH:(i + 1) * self.LOG_MAX_WIDTH] for i in
             xrange(len(msg) / (self.LOG_MAX_WIDTH + 1) + 1)]
        l = reversed(l)
        for line in l:
            if len(self.logMessage) >= self.LOG_MAX:
                self.logMessage.popleft()
            self.logMessage.append(line)

    def drawLog(self):
        i = 1
        for msg in reversed(self.logMessage):
            text = self.font.render(msg, False, (255, 255, 255))  # 描画する文字列の設定
            adjust=4 #そのままだと、最下層のメッセージが欠けるので、これを入れて調整する
            self.screen.blit(text, [0, self.height - adjust - i * self.FONT_SIZE])  # 文字列の表示位置
            i += 1
            print msg
            if i>self.LOG_MAX_VISIBLE:
                break

    def drawSurface(self, char, x, y, x32=True):
        if x32:
            self.screen.blit(char, (x * 32, y * 32))
        else:
            self.screen.blit(char, (x, y))

    def drawImage(self, id, x, y, source, x32=True):
        self.drawSurface(self.imageSources[self.getImageIndex(source)][id], x, y, x32)

    def getImageIndex(self, source):
        if source == "field":
            index = 0
        elif source == "char":
            index = 1
        else:
            message = "Unknown Source : " + source
            raise UnboundLocalError, message
        return index

    def drawMap(self, map, source):
        index = self.getImageIndex(source)
        for x in xrange(mapX):
            for y in xrange(mapY):
                if map[y][x] != -1:
                    self.drawSurface(self.imageSources[index][map[y][x]], x, y)

    def getImageList(self, filename, transparent=False):
        image = self.loadImage(filename, -1)
        imageList = []
        for x in xrange(0, image.get_width(), self.CHIP_SIZE):
            for y in xrange(0, image.get_height(), self.CHIP_SIZE):
                surface = pygame.Surface((self.CHIP_SIZE, self.CHIP_SIZE))
                surface.blit(image, (0, 0), (x, y, self.CHIP_SIZE, self.CHIP_SIZE))
                if transparent:
                    surface.set_colorkey(surface.get_at((0, 0)), RLEACCEL)
                surface.convert()
                imageList.append(surface)
        return imageList

    def update(self):
        self.drawLog()
        pygame.display.update()

    def loadImage(self, filename, colorKey):
        filename = os.path.join("graphics", filename)
        try:
            image = pygame.image.load(filename)
        except pygame.error, message:
            print "Can not load a image"
            raise pygame.error, message
        image = image.convert()
        return image

stage=pygameWrapper(logMaxVisible=4)
