import pyglet
import random
import time
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.window import key
from PIL import Image
window=pyglet.window.Window()

img=pyglet.image.load("graphics/chars.png",decoder=PNGImageDecoder())
print(img.get_image_data())

chars=[]
for char in pyglet.image.ImageGrid(img,img.height//32,img.width//32):
    chars.append(pyglet.sprite.Sprite(char))


keys = []
m=[]
for y in range(12):
    _ = []
    for x in range(16):
        c = chars[random.randint(1, 90)]
        c.x, c.y = x * 32, y * 32
        _.append(c)
    m.append(_)


@window.event
def update(dt):
    if keys:
        global m
        m = []
        for y in range(12):
            _ = []
            for x in range(16):
                c = chars[random.randint(1, 90)]
                c.x, c.y = x * 32, y * 32
                _.append(c)
            m.append(_)
        time.sleep(0.05)
    pass

@window.event
def on_key_press(symbol, modifiers):
    if symbol in keys:
        return
    keys.append(symbol)
    pass

@window.event
def on_key_release(symbol, modifiers):
    if symbol in keys:
        keys.remove(symbol)

@window.event
def on_draw():
    window.clear()
    global m
    for y in range(12):
        for x in range(16):
            m[y][x].draw()

    pass

pyglet.clock.schedule_interval(update, 1/30.)
pyglet.app.run()