import random
from pico2d import *

class Map:
    def __init__(self):
        self.image = load_image('map.png')
        self.moving_image = load_image('moving.png')
        self.x = 400
        self.y = 500
        self.moving_x = 120
        self.moving_y = 480

    def update(self):
        if go:
            self.moving_x+=2
    def draw(self):
        self.image.draw(self.x,self.y)
        self.moving_image.draw(self.moving_x,self.moving_y)

class Enemy_Arrow:
    def __init__(self):
        global stage
        self.x, self.y = 900, 100
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.arrow_image = load_image('arrow.png')
        self.hp = 100 * stage
        self.atk = 100 * stage
        self.attack_time = 0
        self.arrow_x = self.x
        self.arrow_y = self.y
        self.arrow_up = True
        self.arrow_attack = False
        self.arrow_frame= 0
    def arrow_animation(self):
        self.arrow_x -= 10
        if self.arrow_y < 125 and self.arrow_up:
            self.arrow_frame = 0
        elif self.arrow_y < 160 and self.arrow_up:
            self.arrow_frame = 1
        elif self.arrow_y < 200 and self.arrow_up:
            self.arrow_frame = 2
        elif self.arrow_y == 200:
            self.arrow_frame = 3
        elif self.arrow_y < 125:
            self.arrow_frame = 6
        elif self.arrow_y < 160:
            self.arrow_frame = 5
        elif self.arrow_y < 200:
            self.arrow_frame = 4

        if self.arrow_up == True and self.arrow_x >= self.x:
            self.arrow_x = self.x
            self.arrow_y = self.y
        if self.arrow_up:
            self.arrow_y +=5
        else:
            self.arrow_y -= 10
        if self.arrow_up and self.arrow_y >= 200:
            self.arrow_up = False
        for object in team:
            if object.x+20+(object.num*25)>=self.arrow_x-40 and object.x-20+(object.num*25)<= self.arrow_x-40 and self.arrow_y <=130:
                object.hp -= self.atk
                self.arrow_attack = False
                self.arrow_x = 900
                self.arrow_y = 700
                self.arrow_up = True
                self.attack_time = 0
        if self.arrow_y<=90:
            self.arrow_attack = False
            self.arrow_x = 900
            self.arrow_y = 700
            self.arrow_up = True

    def update(self):
        global enemy_count, go,attack,object,team
        self.frame = (self.frame +1) % 8
        self.attack_time += 1
        if go:
                self.x -= 10
                if self.arrow_attack == True:
                    self.arrow_animation()
        if self.hp <= 0:
            self.x = 800
            self.hp = 100
            self.arrow_frame = 0
            self.arrow_x = 900
            self.arrow_y = 700
            self.arrow_up = True
            self.attack_time = 0
            self.arrow_attack = False
        if self.arrow_attack == True:
                self.arrow_animation()
        if self.x > 500:
            self.x -= 10
        else:
            self.attack_time += 1
            if self.attack_time >= 50:
                self.arrow_attack = True
                self.attack_time = 0
            if self.x<=250:
                go = False
                for object in team:
                    if object.num == 2:
                        if attack:
                            self.hp -= object.atk
                            attack = False


    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)
        if self.arrow_attack:
            self.arrow_image.clip_draw(self.arrow_frame*80,0,80,80,self.arrow_x,self.arrow_y)


class Grass:
    def __init__(self):
        self.image = load_image('back_ground.png')
        self.x = 400
        self.num =None
    def draw(self):
        self.image.draw(self.x+800*self.num,300)
    def update(self):
        global go
        if go and self.x > -400:
            self.x -= 10
        elif self.x <= -400:
            self.x = 400

class Enemy:
    def __init__(self):
        global stage
        self.x, self.y = 900, 100
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.hp = 100 * stage
        self.atk = 100 * stage
        self.attack_time = 0
    def update(self):
        global enemy_count, go,attack,object,team
        self.frame = (self.frame +1) % 8
        self.attack_time += 1
        if self.hp <= 0:
            self.x = 800
            self.hp = 100
            self.attack_time = 0
        if self.x > 250:
            self.x -= 10
        else:
            go = False
            for object in team:
                if object.num == 2:
                    if attack:
                        self.hp -= object.atk
                        attack = False
                    if self.attack_time >= 10:
                        object.hp -= self.atk
                        self.attack_time = 0
        if self.x == 300:
            enemy_count += 1
    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)

class Object:
    def __init__(self):
        self.x, self.y = 100, 100
        self.frame = 0
        self.num = None
        self.image = load_image('run_animation.png')
        self.hp = 100
        self.atk = 10
    def update(self):
        if self.hp == 0:
            self.y += 100
            self.hp = 100
        self.frame = (self.frame +1) % 8
        if self.num == 2:
            self.atk = 20
    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x+50*self.num,self.y)

def handle_events():
    global running, go, attack
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            go = True
        elif event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            go = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_z:
            attack = True

attack = False
num=0
stage=1
enemy_count=1
team = None
go = None
object = None
enemy = None
enemy_army = None
map=None
enemy_arrow = None
grass1 = None
grass2 = None
pever = None
running = True

def enter():
    global map, grass1,grass2, team,num,go,enemy,stage,enemy_army,enemy_arrow
    open_canvas()
    team = [Object() for i in range(3)]
    enemy_army = [Enemy() for j in range(10)]
    go = False
    grass1 = Grass()
    grass2 = Grass()
    enemy_arrow = Enemy_Arrow()
    grass1.num = 0
    grass2.num = 1
    pever = 0
    for object in team:
        object.num=num
        num += 1
    map = Map()

def exit():
    global map,boy, grass1,grass2, team,object,enemy,enemy_army,stage,enemy_count,enemy_arrow
    del(object)
    del(enemy_count)
    del(grass1)
    del(grass2)
    del(team)
    del(enemy)
    del(map)
    del(stage)
    del(enemy_army)
    del(enemy_arrow)
    close_canvas()

def update():
    army = 0

    for object in team:
        object.update()
    for enemy in enemy_army:
        enemy.update()
        if army >= enemy_count:
            break
        else:
            army += 1
    enemy_arrow.update()
    map.update()
    grass1.update()
    grass2.update()

def draw():
    clear_canvas()
    grass1.draw()
    grass2.draw()
    enemy_arrow.draw()
    for object in team:
        object.draw()
    for enemy in enemy_army:
        enemy.draw()
    map.draw()
    update_canvas()


def main():
    enter()
    while running:
        handle_events()
        update()
        draw()
        delay(0.05)
    exit()

if __name__ == '__main__':
    main()