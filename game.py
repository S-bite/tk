#coding:utf-8

from item import item
class game():
    def __init__(self,m_field,m_item,actorCtr,m_entity):
        self.field=m_field
        self.item=m_item
        self.actorCtr=actorCtr
        self.entity=m_entity


p=item("portion","drink",10,1)
s=item("sword","attack",30,-1)
_=item("None","None",-1,-1)


