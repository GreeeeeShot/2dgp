import random

from pico2d import *

class Unit:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    run_image = None
    stand_image =None
    attack_image = None
    RUN, STAND, ATTACK = 0, 1, 2

    def __init__(self):
        self.x, self.y = 240, 50
        self.frame = random.randint(0, 5)
        self.total_frames = 0.0
        self.state = self.STAND
        self.attack_frame = 0
        if Unit.run_image == None:
            Unit.run_image = load_image('player_run.png')
        if Unit.stand_image == None:
            Unit.stand_image = load_image('player_stand.png')
        if Unit.attack_image == None:
            Unit.attack_image = load_image('player_attack.png')


    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.total_frames += Unit.FRAMES_PER_ACTION * Unit.ACTION_PER_TIME * frame_time
        self.run_frame = int(self.total_frames) % 6
        self.stand_frame = int(self.total_frames) % 4
        if self.state == self.ATTACK:
            self.attack_frame=(self.attack_frame+1)%120


    def draw(self):
        if self.state == self.RUN:
            self.run_image.clip_draw(self.run_frame*40,0,40,46,self.x+50,self.y)
        elif self.state == self.STAND:
            self.stand_image.clip_draw(self.stand_frame*40,0,40,45,self.x+50,self.y)
        elif self.state == self.ATTACK:
            self.attack_image.clip_draw((int)(self.attack_frame/30)*80,0,80,45,self.x+50,self.y)


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.state in (self.STAND, self.ATTACK):
                self.state = self.RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            if self.state in (self.STAND, self.RUN):
                self.state = self.ATTACK
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.state in (self.RUN,):
                self.state = self.STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_z):
            if self.state in (self.ATTACK,):
                self.state = self.STAND