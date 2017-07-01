import random
class Neuro():
    def __init__(self,input_size=10+25,hide_size=[30,25,20],out_size=[16+2]):
        self.layer=[[] for _ in range(2+len(hide_size))]

        tmp=[]
        tmp.append(random.random() for _ in range(hide_size[0]) )
        self.layer[0].append(tmp)

n=Neuro()
print(n.layer)