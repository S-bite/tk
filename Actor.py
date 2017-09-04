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
import random as rnd


class Actor():
    def __init__(self, data):
        default_data = {"is_player":True,"act_state": -1, "act_id": -1, "name": "-1", "image": -1, "race": "-1", "job": "-1",
                        "HP_MAX": -1,"HP": -1, "MP_MAX": -1, "MP": -1, "STR": -1, "DEF": -1, "SPD": -1, "state": -1,
                        "x": -1, "y": -1, "items":[]}
        default_data.update(data)
        data = default_data
        for d in data:
            setattr(self, d, data[d])


# noinspection PyUnresolvedReferences
class Enemy(Actor):
        def __init__(self,data):
            default_data = {"is_player":False,"move_type": 0, "dist": 3, "target": None, "tactics": {0: ["attack", 80], 1: ["heal", 20],
                                                                                   2: ["throw", 0],   3: ["beg", 0]}, }
            default_data.update(data)
            data = default_data
            Actor.__init__(self, data)

        def get_action(self):
            if self.target == None:
                if self.move_type == 0:
                    return {"action": "move_random","target_id":self.act_id}
                if self.move_type == 1:
                    return {"action": "none","target_id":self.act_id}
            if abs(self.target.x-self.x)+abs(self.target.y-self.y) != self.dist:
                 return {"action": "move","target_id":self.target.act_id}

            tactics = [self.tactics[i][0] for i in self.tactics]
            weights = [self.tactics[i][1] for i in self.tactics]
            return {"action": rnd.choices(tactics, weights)[0],"target_id":self.target.act_id,}

        #    checkDict = ["tactics"]
        #    if [hasattr(self, x) and not isinstance((self, x),types.FunctionType)  for x in checkDict].count(
        #            False) != 0:
        #        raise (BaseException("necessary variable is not defined"))
        pass
# noinspection PyUnresolvedReferences
class Player(Actor):
    def __init__(self, data):
        Actor.__init__(self, data)

    def get_action(self):
       return {"action": "player","target_id":self.act_id if self.target==None else self.target.act_id}
