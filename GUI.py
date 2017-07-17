import pyglet
import random
import time
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.window import key
from PIL import Image
from ActorController import ActorController
from game import game
from Actor import Player,Enemy,Actor
from field import field
class GUI():
    def __init__(self,game):
        self.game=game
        self.game.step()
        self.window=pyglet.window.Window()

    def run(self):
#        pyglet.clock.schedule_interval(update, 1/30.)
        pyglet.app.run()
room1Act=ActorController()
p=Player({"name":"Player","SPD":20,"HP":100,"STR":150,"DEF":5,"x":5,"y":5})
room1Act.addActorAsPlayer(p)
room1Act.addActor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":8,"y":1,"dist":1}),target=room1Act.player)
room1Act.addActor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":3,"y":4,"dist":1}),target=room1Act.player)

room1Map=field(name="room1")
room1Map.door[1][1]=["room2",8,8]

gm=game([{"field":room1Map,"ActorController":room1Act}])
g=GUI(gm)
g.main()