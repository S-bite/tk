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
from utils import clip_array

class GUI():
    GUI_width=800
    GUI_height=640
    GUI_map_height=480
    window = pyglet.window.Window(GUI_width,GUI_height)

    def __init__(self,game):

        img=pyglet.image.load("graphics/back.png",decoder=PNGImageDecoder())
        self.BACK_IMAGE=img.get_region(0,0,self.GUI_width,self.GUI_height-self.GUI_map_height)
        self.CHAR_IMAGES=[]
        img=pyglet.image.load("graphics/chars.png",decoder=PNGImageDecoder())
        #img.get_image_data()
        for char in pyglet.image.ImageGrid(img,img.height//32,img.width//32):
            self.CHAR_IMAGES.append(char)

        self.TERRAIN_IMAGES = []
        img = pyglet.image.load("graphics/chip12e_map_fall.png", decoder=PNGImageDecoder())
        #img.get_image_data()
        for terrain in pyglet.image.ImageGrid(img, img.height // 32, img.width // 32):
            self.TERRAIN_IMAGES.append(terrain)
        self.was_game_changed=True
        self.game=game
        self.keys=key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    @window.event
    def on_draw():
        pass
    @window.event
    def update(self,_):
        #draw game
        if self.was_game_changed==False:
            return 0
        glEnable(GL_BLEND)
        field=self.game.field_map
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.window.clear()


        #draw terrain
        player_x=self.game.actor_ctr.player.x
        player_y=self.game.actor_ctr.player.y
        clipped_image_id=clip_array(field.image,player_x, player_y,self.GUI_width//32,self.GUI_map_height//32)
        for y,_ in enumerate(clipped_image_id):
            for x,image_id in enumerate(_):
                if image_id!=-1:
                    self.TERRAIN_IMAGES[image_id].blit(x*32,self.GUI_height-(y+1)*32)

        #draw door
        clipped_door=clip_array(field.door,player_x, player_y,self.GUI_width//32,self.GUI_map_height//32,pad_value=None)
        for y,_ in enumerate(clipped_door):
            for x,door in enumerate(_):
                if door!=None:
                    #replace 18 to door image id
                    self.TERRAIN_IMAGES[18].blit(x*32,self.GUI_height-(y+1)*32)
        #draw actor
        actors=self.game.actor_ctr.actors.values()
        def relative_x(x):
            return (self.GUI_width//(32*2)-player_x+x)*32
        def relative_y(y):
            return self.GUI_height-(self.GUI_map_height//(32*2)-player_y+y+1)*32

        for actor in actors:
            self.CHAR_IMAGES[actor.image].blit(relative_x(actor.x) ,relative_y(actor.y))


        label = pyglet.text.Label('',
        font_size=36,
        x=self.GUI_width//2, y=self.GUI_height//2,
        anchor_x='center', anchor_y='center')
        label.draw()
        self.BACK_IMAGE.blit(0,0)
    @window.event
    def input(self,_):

        in_keys=[]
        for k in self.keys:
            if  self.keys[k]==True:
                in_keys.append(key._key_names[k])
        #because it's an asyncronous
        if in_keys==[]:
            return
        res= self.game.step(in_keys)
        if self.was_game_changed==False:
            self.was_game_changed=res

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/30)
        pyglet.clock.schedule_interval(self.input, 1/10)
        pyglet.app.run()
