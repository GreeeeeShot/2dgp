__author__ = 'Administrator'
from pico2d import *

class Hp_Bar:

    image = None

    def __init__(self):
        if Hp_Bar.image == None :
            Hp_Bar.image = load_image('hp_bar.png')
        self.x=100
        self.first_hp = 3000
        self.last_hp = 0

    def draw(self):
        Hp_Bar.image.clip_draw_to_origin(10,0,10,10,(self.x-50)+(self.last_hp/100),100,(self.first_hp-self.last_hp)/100,10)
        Hp_Bar.image.clip_draw_to_origin(0,0,10,10,(self.x-50),100,(self.last_hp/100),10)


def test_hp_bar():
    open_canvas()
    hp_bar = Hp_Bar()
    for a in range (3000):
        hp_bar.last_hp = 3000-a
        clear_canvas()
        hp_bar.draw()
        update_canvas()
    print('%d , %d , %d' % ((hp_bar.last_hp/100),300+(hp_bar.last_hp/100),((hp_bar.first_hp-hp_bar.last_hp)/100)))
    close_canvas()

if __name__=='__main__':
    test_hp_bar()