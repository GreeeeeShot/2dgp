import random

from pico2d import *

class Enemy_Knight:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    run_image = None
    stand_image =None
    attack_image = None
    RUN, STAND, ATTACK = 0, 1, 2

    def __init__(self):
        self.x, self.y = 700, 70
        self.frame = random.randint(0, 5)
        self.total_frames = 0.0
        self.state = self.RUN
        self.attack_frame = 0
        if Enemy_Knight.run_image == None:
            Enemy_Knight.run_image = load_image('knight_run.png')
        if Enemy_Knight.stand_image == None:
            Enemy_Knight.stand_image = load_image('player_stand.png')
        if Enemy_Knight.attack_image == None:
            Enemy_Knight.attack_image = load_image('player_attack.png')

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.total_frames += Enemy_Knight.FRAMES_PER_ACTION * Enemy_Knight.ACTION_PER_TIME * frame_time
        self.run_frame = int(self.total_frames) % 8
        self.stand_frame = int(self.total_frames) % 4
        if self.state == self.ATTACK:
            self.attack_frame=(self.attack_frame+1)%120

    def draw(self):
        if self.state == self.RUN:
            self.run_image.clip_draw(self.run_frame*64,0,64,88,self.x,self.y)
        # elif self.state == self.STAND:
        #     self.stand_image.clip_draw(self.stand_frame*40,0,40,45,self.x+50,self.y)
        # elif self.state == self.ATTACK:
        #     self.attack_image.clip_draw((int)(self.attack_frame/30)*80,0,80,45,self.x+50,self.y)


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50