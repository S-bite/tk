import pyglet
import random
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.window import key
from PIL import Image
from ActorController import ActorController
from game import game
from Actor import Player,Enemy,Actor
from field import field
import time
class GUI():
    def __init__(self,game):
        self.game=game
        #self.game.step()
        print(key._key_names)
        self.window=pyglet.window.Window()
        self.keys=key.KeyStateHandler()
        self.window.push_handlers(self.keys)
    def update(self,_):
        pass
    def input(self,_):
        res=[]
        for k in self.keys:
            if  self.keys[k]==True:
                res.append(key._key_names[k])
        if True:#res:
            self.game.step(res)
            print(res)
            time.sleep(0.25)
    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/30)
        pyglet.clock.schedule_interval(self.input, 1/100)
        pyglet.app.run()
room1_act=ActorController()
p=Player({"name":"Player","SPD":20,"HP":100,"STR":150,"DEF":5,"x":5,"y":5})
room1_act.add_actor_as_player(p)
room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":8,"y":1,"dist":1}),target=room1_act.player)
room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":3,"y":4,"dist":1}),target=room1_act.player)

room1_map=field(name="room1")
room1_map.door[1][1]=["room2",8,8]

room2_act = ActorController()
p = Player({"name": "Player", "SPD": 20, "HP": 100, "STR": 150, "DEF": 5, "x": 5, "y": 5})
room2_act.add_actor_as_player(p)
room2_act.add_actor(Enemy({"name": "bat", "SPD": 10, "HP": 5, "STR": 10, "DEF": 8, "x": 1, "y": 1, "dist": 1}),
                    target=room2_act.player)
room2_act.add_actor(Enemy({"name": "bat", "SPD": 10, "HP": 5, "STR": 10, "DEF": 8, "x": 8, "y": 1, "dist": 1}),
                    target=room2_act.player)

room2_map = field(name="room2")
room2_map.createBoarder()
room2_map.door[8][8] = ["room1", 1, 1]

gm = game([{"field": room1_map, "ActorController": room1_act}, {"field": room2_map, "ActorController": room2_act}], 1)
g=GUI(gm)
g.run()