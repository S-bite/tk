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
from pyglet.gl import *
import time
class GUI():
    window = pyglet.window.Window()

    def __init__(self,game):

        self.CHAR_IMAGES=[]
        img=pyglet.image.load("graphics/chars.png",decoder=PNGImageDecoder())
        img.get_image_data()
        for char in pyglet.image.ImageGrid(img,img.height//32,img.width//32):
            self.CHAR_IMAGES.append(char)

        self.TERRAIN_IMAGES = []
        img = pyglet.image.load("graphics/chip12e_map_fall.png", decoder=PNGImageDecoder())
        img.get_image_data()
        for terrain in pyglet.image.ImageGrid(img, img.height // 32, img.width // 32):
            self.TERRAIN_IMAGES.append(terrain)

        self.game=game
        print(key._key_names)
        self.keys=key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    @window.event
    def on_draw():
        pass
    @window.event
    def update(self,_):
        #draw game
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.window.clear()


        #draw terrain
        field=self.game.field_map
        for x,_ in enumerate(field.terrain):
            for y,terrain in enumerate(_):
                if terrain==0:
                    self.TERRAIN_IMAGES[47].blit(x*32,field.height*32-y*32)
                elif terrain==1:
                    self.TERRAIN_IMAGES[5].blit(x*32,field.height*32-y*32)
        for x, _ in enumerate(field.door):
            for y, door in enumerate(_):
                if door:
                    self.TERRAIN_IMAGES[14].blit(x * 32, field.height*32-y * 32)

        #draw actor
        actors=self.game.actor_ctr.actors.values()
        for actor in actors:
            self.CHAR_IMAGES[actor.image].blit(actor.x*32,field.height*32-actor.y*32)

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

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/30)
        pyglet.clock.schedule_interval(self.input, 1/10)
        pyglet.app.run()

room1_act=ActorController()
room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":8,"y":1,"dist":1,"image":258}),target=room1_act.player)
room1_act.add_actor(Enemy({"name":"rat","SPD":10,"HP":10,"STR":5,"DEF":5,"x":3,"y":4,"dist":1,"image":267}),target=room1_act.player)

room1_map=field(name="room1")
room1_map.door[1][1]=["room2",8,8]

room2_act = ActorController()
p = Player({"name": "Player", "SPD": 20, "HP": 100, "STR": 150, "DEF": 5, "x": 5, "y": 5,"image":282})
room2_act.add_actor_as_player(p)
room2_act.add_actor(Enemy({"name": "bat", "SPD": 10, "HP": 5, "STR": 10, "DEF": 8, "x": 1, "y": 1, "dist": 1,"image":258}),
                    target=room2_act.player)
room2_act.add_actor(Enemy({"name": "bat", "SPD": 10, "HP": 5, "STR": 10, "DEF": 8, "x": 8, "y": 1, "dist": 1,"image":267}),
                    target=room2_act.player)

room2_map = field(name="room2")
room2_map.create_boarder()
room2_map.door[8][8] = ["room1", 1, 1]

gm = game([{"field": room1_map, "ActorController": room1_act}, {"field": room2_map, "ActorController": room2_act}], 1)
g=GUI(gm)
g.run()