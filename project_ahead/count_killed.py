from pico2d import *

class Count_Killed:
    num_image = None

    def __init__(self):
        self.ck = 0
        if Count_Killed.num_image == None:
            Count_Killed.num_image = load_image("num.png")

    def count(self):
        self.ck += 1

    def clear(self):
        self.ck = 0

    def draw(self):
        self.num_image.clip_draw((self.ck%10)*16,0,16,32,50,350)
        self.num_image.clip_draw((int(self.ck/10)%10)*16,0,16,32,35,350)
        self.num_image.clip_draw(int(self.ck/100)*16,0,16,32,20,350)