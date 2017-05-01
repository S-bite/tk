# coding:utf-8

"""
class:NPC

パラメータ
    体力
    満腹度
    睡眠度
    年齢
    お金
    種の数
    植えている種
    (種の成長度)
    毛皮の数
    食べ物の数

分かる情報
    自分のパラメータ
    周りのモンスター

行動
    作物を植える
    作物を収穫する
    モンスターを倒す
    種を売る
    作物を売る
    毛皮を売る
    眠る
    何もしない
"""

import random
class NPC:
    def __init__(self):
        self.HP=100
        self.satiety=100
        self.age=10
        self.money=0
        self.seed=1
        self._plant=[]
        self.fur=0
        self.crop=0
    def seed_update(self):
        for i in xrange(len(self._plant)):
            self._plant[i]+=1
    def plant_seed(self):
        if self.seed<=0:
            print "no seed"
            return
        self.seed-=1
        self._plant.append(0)

    def harvest_crop(self):
        for i in xrange(len(self._plant)):
            if self._plant[i]>=5:
                self._plant[i]=-1
                self.crop+=1
                self.seed+=random.randint(1,3)
        while -1 in self._plant: self._plant.remove(-1)

    def none(self):
        self.seed_update()
    def print_state(self):
        print "HP:",self.HP
        print "satiety:", self.satiety
        print "age:", self.age
        print "money:", self.money
        print "seed:", self.seed
        print "_plant:", self._plant
        print "fur:", self.fur
        print "crop:", self.crop



p=NPC()
for i in xrange(50):
    for j in xrange(p.seed):
        p.plant_seed()
    p.none()
    p.none()
    p.none()
    p.none()
    p.none()
    p.harvest_crop()
    p.print_state()





