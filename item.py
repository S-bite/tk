#coding:utf-8
d_effect_to_int={"heal":1,"damage":2}
class item():
    def __init__(self,name,effect,power,turn):
        self.name=name
        self.effect=effect
        self.power=power
        self.turn=turn
        self.data=[name,effect,power,turn]


portion=item("heal portion","heal",12,30)
print(portion.data)
