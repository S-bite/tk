#coding:utf-8
"""
Actor:
id
x,y
worldX,worldY
image
name
race
job
HP
MP
STR
DEF
SPD
...
数値は辞書形式で格納
param={HP=10,STR=3...}
foo=Actor(param)
"""
import types

class Actor():
    def __init__(self,data={}):
        defaultData={"actState":-1,"actId":-1,"name":"-1","image":-1,"race":"-1","job":"-1","HP_MAX":-1,"HP":-1,
            "MP_MAX":-1,"MP":-1,"STR":-1,"DEF":-1,"SPD":-1,"state":-1,"x":-1,"y":-1}
        defaultData.update(data)
        data=defaultData
        for d in data:
            setattr(self,d,data[d])

        #checkDict=["actState","actId","name","image","race","job","HP_MAX","HP","MP_MAX","MP","STR","DEF","SPD","state",
        #        "x","y"]
        #if [hasattr(self,x) and not isinstance((self, x),types.FunctionType) for x in checkDict] .count(False)!=0:
        #    raise ("necessary variable is not defined")

class Enemy(Actor):
        def __init__(self,data={}):
            defaultData = {"tactics":{0:"attack",1:"heal",2:"throw",3:"beg"},"neuro":[]}
            defaultData.update(data)
            data=defaultData
            Actor.__init__(self,data)

         #   checkDict = ["tactics"]
         #   if [hasattr(self, x) and not isinstance((self, x),types.FunctionType)  for x in checkDict].count(
         #           False) != 0:
         #       raise (BaseException("necessary variable is not defined"))


        pass

class Player(Actor):
    pass
