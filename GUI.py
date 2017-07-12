import pyglet
import random
import time
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.window import key
from PIL import Image
class GUI():
    def __init__(self):
        self.window=pyglet.window.Window()

    def run(self):
#        pyglet.clock.schedule_interval(update, 1/30.)
        pyglet.app.run()

g=GUI()
g.main()