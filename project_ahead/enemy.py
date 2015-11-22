import random

from pico2d import *

class Enemy_Knight:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    run_image = None
    stand_image =None
    attack_image = None
    dead_image =None
    speed=TIME_PER_ACTION
    RUN, STAND, ATTACK, DEAD = 0, 1, 2, 3

    def __init__(self):
        self.x, self.y = 700, 70
        self.total_frames = 0.0
        self.state = self.RUN
        self.attack_frame = 0
        self.dead_frame = 0
        self.atk = 5
        self.wait = 0.0
        self.hp = 3000
        if Enemy_Knight.run_image == None:
            Enemy_Knight.run_image = load_image('knight_run.png')
        if Enemy_Knight.stand_image == None:
            Enemy_Knight.stand_image = load_image('knight_stand.png')
        if Enemy_Knight.attack_image == None:
            Enemy_Knight.attack_image = load_image('knight_attack.png')
        if Enemy_Knight.dead_image == None:
            Enemy_Knight.dead_image = load_image('knight_dead.png')

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))
        self.total_frames += Enemy_Knight.FRAMES_PER_ACTION * Enemy_Knight.ACTION_PER_TIME * frame_time
        self.run_frame = int(self.total_frames) % 8
        self.stand_frame = int(self.total_frames) % 11
        if self.state == self.RUN:
            self.x -= self.speed
        if self.hp <=0:
            self.state = self.DEAD
            self.dead()
        if self.state == self.ATTACK:
            self.attack()
        if self.wait == 0.0 :
            self.wait = int(self.total_frames)
        if (int(self.total_frames-self.wait) >= 20) and (self.wait != 0.0) and (self.state == self.STAND) :
            self.state = self.ATTACK
            self.attack_frame = 0
            self.wait =int(self.total_frames)
        print (self.dead_frame)

    def draw(self):
        if self.state == self.RUN:
            self.run_image.clip_draw(self.run_frame*64,0,64,88,self.x,self.y)
        elif self.state == self.STAND:
            self.stand_image.clip_draw(self.stand_frame*56,0,56,90,self.x,self.y)
        elif self.state == self.ATTACK:
            self.attack_image.clip_draw(self.attack_frame*108,0,108,88,self.x,self.y)
        elif self.state == self.DEAD:
             self.dead_image.clip_draw(self.dead_frame*96,0,96,88,self.x,self.y)
        self.draw_bb()

    def dead(self):
        self.dead_frame=int(self.total_frames-self.wait)%9
        if self.dead_frame>=8:
            self.dead_frame = 0
            self.state = self.RUN
            self.x = 800
            self.hp=3000
            self.speed = self.TIME_PER_ACTION
            self.wait = 0.0

    def attack_damage(self,unit):
        unit.hp -= self.atk

    def attack(self):
        self.attack_frame=int(self.total_frames-self.wait)%12
        if self.attack_frame>=11:
            #self.state = self.STAND
            self.attack_frame = 0
            self.state = self.STAND
            self.wait = 0

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 40

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                if self.speed>0:
                    self.speed += Enemy_Knight.TIME_PER_ACTION
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if self.speed>Enemy_Knight.TIME_PER_ACTION:
                    self.speed -= Enemy_Knight.TIME_PER_ACTION