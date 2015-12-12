import random

from pico2d import *

class Unit:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    run_image = None
    stand_image =None
    attack_image = None
    dead_image = None

    RUN, STAND, ATTACK, DEAD = 0, 1, 2, 3

    hp_image = None

    def __init__(self):
        self.x, self.y = 240, 50
        self.frame = random.randint(0, 5)
        self.total_frames = 0.0
        self.state = self.STAND
        self.attack_frame = 0
        self.dead_frame = 0
        self.atk = 10
        self.hp = 35000
        self.check_run = False
        self.wait = 0.0
        if Unit.run_image == None:
            Unit.run_image = load_image('player_run.png')
        if Unit.stand_image == None:
            Unit.stand_image = load_image('player_stand.png')
        if Unit.attack_image == None:
            Unit.attack_image = load_image('player_attack.png')
        if Unit.hp_image == None :
           Unit.hp_image = load_image('hp_bar.png')
        self.first_hp = self.hp
        if Unit.dead_image == None:
            Unit.dead_image = load_image('player_dead.png')


    def update(self, frame_time,stage):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))

        self.total_frames += Unit.FRAMES_PER_ACTION * Unit.ACTION_PER_TIME * frame_time
        self.run_frame = int(self.total_frames) % 6
        self.stand_frame = int(self.total_frames) % 4
        if self.state == self.ATTACK:
            self.attack()
        if self.hp<=0:
           if  self.wait == 0.0 :
                self.wait=self.total_frames
           self.dead(stage)


    def attack_damage(self,enemy):
        if self.state == self.ATTACK and enemy.hp>0 :
            enemy.hp -= self.atk

    def attack(self):
        self.attack_frame+=1
        if self.attack_frame>=120:
            if self.check_run:
                self.state = self.RUN
            else:
                self.state = self.STAND
            self.attack_frame = 0

    def draw(self):
        if self.state == self.RUN:
            self.run_image.clip_draw(self.run_frame*40,0,40,46,self.x,self.y)
        elif self.state == self.STAND:
            self.stand_image.clip_draw(self.stand_frame*40,0,40,45,self.x,self.y)
        elif self.state == self.ATTACK:
            self.attack_image.clip_draw((int)(self.attack_frame/30)*80,0,80,45,self.x,self.y)
        elif self.state == self.DEAD:
            self.dead_image.clip_draw(self.dead_frame*52,0,52,44,self.x,self.y)
        self.draw_bb()
        Unit.hp_image.clip_draw_to_origin(10,0,10,10,self.x-20+(self.hp/800),80,(self.first_hp-self.hp)/800,10)
        Unit.hp_image.clip_draw_to_origin(0,0,10,10,self.x-20,80,(self.hp/800),10)


    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_event(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.check_run = True
            if self.state in (self.STAND, self.ATTACK):
                self.state = self.RUN
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            if self.state in (self.STAND, self.RUN):
                self.state = self.ATTACK
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            self.check_run = False
            if self.state in (self.RUN,self.ATTACK):
                self.state = self.STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_z):
            if self.check_run:
                self.state = self.RUN

    def dead(self,stage):
        self.dead_frame = (int)(self.total_frames - self.wait)%4
        self.state = Unit.DEAD
        if self.dead_frame>=3:
            self.hp = stage*40000
            self.atk = stage*5+5
            self.first_hp = self.hp
            self.dead_frame = 0
            self.state = self.STAND
