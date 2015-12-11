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
    hp_image = None

    def __init__(self):
        self.x, self.y = 700, 70
        self.total_frames = 0.0
        self.state = self.RUN
        self.attack_frame = 0
        self.dead_frame = 0
        self.atk = 2
        self.wait = 0.0
        self.hp = 3000
        self.check_dead = False
        if Enemy_Knight.run_image == None:
            Enemy_Knight.run_image = load_image('knight_run.png')
        if Enemy_Knight.stand_image == None:
            Enemy_Knight.stand_image = load_image('knight_stand.png')
        if Enemy_Knight.attack_image == None:
            Enemy_Knight.attack_image = load_image('knight_attack.png')
        if Enemy_Knight.dead_image == None:
            Enemy_Knight.dead_image = load_image('knight_dead.png')
        if Enemy_Knight.hp_image == None :
           Enemy_Knight.hp_image = load_image('hp_bar.png')
        self.first_hp = self.hp

    def update(self, frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))
        self.total_frames += Enemy_Knight.FRAMES_PER_ACTION * Enemy_Knight.ACTION_PER_TIME * frame_time
        self.run_frame = int(self.total_frames) % 8
        self.stand_frame = int(self.total_frames) % 11
        if self.state == self.RUN:
            self.x -= self.speed
        if self.hp <=0:
            self.hp=0;
            self.state = self.DEAD
            self.check_dead = self.dead()
        if self.state == self.ATTACK:
            self.attack()
        if self.wait == 0.0 :
            self.wait = int(self.total_frames)
        if (int(self.total_frames-self.wait) >= 20) and (self.wait != 0.0) and (self.state == self.STAND) :
            self.state = self.ATTACK
            self.attack_frame = 0
            self.wait =int(self.total_frames)
        if self.check_dead:
            self.check_dead=False
            return True


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
        Enemy_Knight.hp_image.clip_draw_to_origin(10,0,10,10,self.x-20+(self.hp/100),100,(self.first_hp-self.hp)/100,10)
        Enemy_Knight.hp_image.clip_draw_to_origin(0,0,10,10,self.x-20,100,(self.hp/100),10)

    def dead(self):
        self.dead_frame=int(self.total_frames-self.wait)%9
        if self.dead_frame>=8:
            self.dead_frame = 0
            self.state = self.RUN
            self.x = 800
            self.hp=3000
            self.speed = Enemy_Knight.TIME_PER_ACTION
            self.wait = 0.0
            return True

    def attack_damage(self,unit):
        unit.hp -= self.atk

    def attack(self):
        self.attack_frame=int(self.total_frames-self.wait)%12
        if self.attack_frame>=11:
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
            # if event.key == SDLK_z:
            #     if self.speed>=Enemy_Knight.TIME_PER_ACTION*2:
            #         self.speed -= Enemy_Knight.TIME_PER_ACTION
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if self.speed>Enemy_Knight.TIME_PER_ACTION:
                    self.speed -= Enemy_Knight.TIME_PER_ACTION

class Enemy_Archur:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    run_image = None
    stand_image =None
    attack_image = None
    dead_image =None
    speed=TIME_PER_ACTION
    RUN, STAND, ATTACK, DEAD = 0, 1, 2, 3
    hp_image = None

    def __init__(self):
        self.x, self.y = 700, 70
        self.total_frames = 0.0
        self.state = self.RUN
        self.attack_frame = 0
        self.dead_frame = 0
        self.atk = 1
        self.wait = 0.0
        self.hp = 3000
        self.check_dead = False
        if Enemy_Archur.run_image == None:
            Enemy_Archur.run_image = load_image('archur_run.png')
        if Enemy_Archur.stand_image == None:
            Enemy_Archur.stand_image = load_image('archur_stand.png')
        if Enemy_Archur.attack_image == None:
            Enemy_Archur.attack_image = load_image('archur_attack.png')
        if Enemy_Archur.dead_image == None:
            Enemy_Archur.dead_image = load_image('archur_dead.png')
        if Enemy_Archur.hp_image == None :
           Enemy_Archur.hp_image = load_image('hp_bar.png')
        self.first_hp = self.hp

    def update(self, frame_time,):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))
        self.total_frames += Enemy_Archur.FRAMES_PER_ACTION * Enemy_Archur.ACTION_PER_TIME * frame_time
        self.run_frame = int(self.total_frames) % 10
        self.stand_frame = int(self.total_frames) % 7
        #if self.state == self.RUN:
        self.x -= self.speed
        if self.hp <=0:
            self.state = self.DEAD
            self.check_dead = self.dead()
        if self.state == self.ATTACK:
            self.attack()
        if self.wait == 0.0 :
            self.wait = int(self.total_frames)
        if (int(self.total_frames-self.wait) >= 50) and (self.wait != 0.0) and (self.state == self.STAND) :
            self.state = self.ATTACK
            self.attack_frame = 0
            self.wait =int(self.total_frames)
        if self.check_dead:
            self.check_dead=False
            return True

    def draw(self):
        if self.state == self.RUN:
            self.run_image.clip_draw(self.run_frame*45,0,45,72,self.x,self.y)
        elif self.state == self.STAND:
            self.stand_image.clip_draw(self.stand_frame*38,0,38,72,self.x,self.y)
        elif self.state == self.ATTACK:
            self.attack_image.clip_draw(self.attack_frame*50,0,50,72,self.x,self.y)
        elif self.state == self.DEAD:
             self.dead_image.clip_draw(self.dead_frame*48,0,48,72,self.x,self.y)
        self.draw_bb()
        Enemy_Archur.hp_image.clip_draw_to_origin(10,0,10,10,self.x-10+(self.hp/100),110,(self.first_hp-self.hp)/100,10)
        Enemy_Archur.hp_image.clip_draw_to_origin(0,0,10,10,self.x-10,110,(self.hp/100),10)

    def dead(self):
        self.dead_frame=int(self.total_frames-self.wait)%7
        if self.dead_frame>=6:
            self.dead_frame = 0
            self.state = self.RUN
            self.x = 800
            self.hp=3000
            self.speed = Enemy_Archur.TIME_PER_ACTION
            self.wait = 0.0
            return True

    def attack_damage(self,unit):
        unit.hp -= self.atk

    def attack(self):
        self.attack_frame=int(self.total_frames-self.wait)%10
        if self.attack_frame>=9:
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
                if self.speed>=0:
                    self.speed += Enemy_Archur.TIME_PER_ACTION
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if self.speed>=Enemy_Archur.TIME_PER_ACTION:
                    self.speed -= Enemy_Archur.TIME_PER_ACTION

class Arrow:
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 7

    image = None

    ATTACK, HIT, REST = 0, 1, 2

    def __init__(self):
        self.x=1000
        self.y=1000
        self.total_frames = 0.0
        self.arrow_up = True
        self.main_frame = 0
        self.draw_frame = 0
        self.start_time = 0.0
        self.state = Arrow.REST
        if Arrow.image == None:
            Arrow.image = load_image("arrow.png")


    def update(self,frame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))
        self.total_frames += Enemy_Archur.FRAMES_PER_ACTION * Enemy_Archur.ACTION_PER_TIME * frame_time
        if self.start_time ==0.0:
            self.start_time = self.total_frames
        if self.state==Arrow.ATTACK:
            self.attack()
        if self.state == Arrow.HIT:
            self.hit()


    def attack(self):
        #if self.total_frames-self.start_time>10:
        self.x -= 1
        if self.y>=200:
            self.arrow_up = False
        if self.arrow_up:
            self.y +=1
        else:
            self.y -= 1
        if self.y < 125 and self.arrow_up:
            self.draw_frame = 0
        elif self.y < 160 and self.arrow_up:
            self.draw_frame = 1
        elif self.y < 200 and self.arrow_up:
            self.draw_frame = 2
        elif self.y >= 200:
            self.draw_frame = 3
        elif self.y < 125:
            self.draw_frame = 6
        elif self.y < 160:
            self.draw_frame = 5
        elif self.y < 200:
            self.draw_frame = 4

    def hit_damage(self,unit,enemy_archur):
        unit.hp -= enemy_archur.atk

    def hit(self):
        self.state = Arrow.REST

    def draw(self):
        if self.state == Arrow.ATTACK:
            self.image.clip_draw(self.draw_frame*80,0,80,80,self.x,self.y)
            self.draw_bb()

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 30, self.y - 40 + ((self.x-100)/7)-10, self.x - 10, self.y - 20+ ((self.x-100)/7)-10
