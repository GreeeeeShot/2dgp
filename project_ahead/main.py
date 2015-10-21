import random
from pico2d import *


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
        self.x = 400
        self.num =None
    def draw(self):
        self.image.draw(self.x+800*self.num,30)
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
        self.atk = 5 * stage
        self.attack_time = 0
    def update(self):
        global enemy_count, go,attack,object,team
        self.frame = (self.frame +1) % 8
        self.attack_time += 1
        if self.hp <= 0:
            self.x = 800
            self.hp = 100
        if self.x > 250:
            self.x -= 10
        else:
            go = False
            for object in team:
                if attack and object.num == 2:
                    self.hp -= object.atk
                    attack = False
                if self.attack_time >= 30 and object.num == 2:
                    object.hp -= self.atk
                    self.attack_time = 0
        if self.x == 300:
            enemy_count += 1
    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x,self.y)

class Object:
    def __init__(self):
        self.go = random.randint(1,2)
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
        if self.num == 0:
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
grass1 = None
grass2 = None
running = True

def enter():
    global grass1,grass2, team,num,go,enemy,stage,enemy_army
    open_canvas()
    team = [Object() for i in range(3)]
    enemy_army = [Enemy() for j in range(100)]
    go = False
    grass1 = Grass()
    grass2 = Grass()
    grass1.num = 0
    grass2.num = 1
    for object in team:
        object.num=num
        num += 1

def exit():
    global boy, grass1,grass2, team,object,enemy,enemy_army,stage,enemy_count
    del(object)
    del(enemy_count)
    del(grass1)
    del(grass2)
    del(team)
    del(enemy)
    del(stage)
    del(enemy_army)
    close_canvas()

def update():
    army = 0
    grass1.update()
    grass2.update()
    for object in team:
        object.update()
    for enemy in enemy_army:
        enemy.update()
        if army >= enemy_count:
            break
        else:
            army += 1

def draw():
    clear_canvas()
    grass1.draw()
    grass2.draw()
    for object in team:
        object.draw()
    for enemy in enemy_army:
        enemy.draw()
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