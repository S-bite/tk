import pyglet
import random
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.window import key
import pyglet.window
from pyglet import sprite
from PIL import Image
from ActorController import ActorController
from game import game
from Actor import Player,Enemy,Actor
from field import field
import time
class GUI():
    window = pyglet.window.Window()

    def __init__(self,game):

        self.CHAR_IMAGES=[]
        img=pyglet.image.load("graphics/chars.png",decoder=PNGImageDecoder())
        img.get_image_data()
        for char in pyglet.image.ImageGrid(img,img.height//32,img.width//32):
            self.CHAR_IMAGES.append(pyglet.sprite.Sprite(char))
        self.game=game
        print(key._key_names)
        self.keys=key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    @window.event
    def update(self,_):
        pass

    @window.event
    def input(self,_):
        res=[]
        for k in self.keys:
            if  self.keys[k]==True:
                res.append(key._key_names[k])
        if True:
            game_data=self.game.step(res)
            if game_data==-1:
                return
            self.window.clear()
            for x,_ in enumerate(game_data.field_map.terrain):
                for y,terrain in enumerate(_):
                    chip=self.CHAR_IMAGES[terrain*10]
                    chip.x=x*32
                    chip.y=y*32
                    chip.draw()
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
room2_map.create_boarder()
room2_map.door[8][8] = ["room1", 1, 1]

gm = game([{"field": room1_map, "ActorController": room1_act}, {"field": room2_map, "ActorController": room2_act}], 1)
g=GUI(gm)
g.run()