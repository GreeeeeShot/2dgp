import random
from pico2d import *

class Pever_Time:
    def __init__(self):
        self.success_image = load_image('pever.png')
        self.fail_image = load_image('fail.png')
        self.x = 400
        self.y = 300

    def draw(self):
        if pever == 1:
            self.success_image.draw(self.x,self.y)
        elif pever == 2:
            self.fail_image.draw(self.x,self.y)

class Map:
    def __init__(self):
        self.image = load_image('map.png')
        self.moving_image = load_image('moving.png')
        self.x = 400
        self.y = 500
        self.moving_x = 120
        self.moving_y = 480

    def update(self):
        global pever,running
        if go:
            self.moving_x+=2
        if self.moving_x >= 500:
            pever = 1
        if self.moving_x >= 670:
            running = False
    def draw(self):
        self.image.draw(self.x,self.y)
        self.moving_image.draw(self.moving_x,self.moving_y)

class Enemy_Arrow:
    def __init__(self):
        global stage
        self.x, self.y = 900, 82
        self.frame = 0
        self.image = load_image('archur_moving.png')
        self.attack_image= load_image('archur_attack.png')
        self.dead_image = load_image('archur_dead.png')
        self.arrow_image = load_image('arrow.png')
        self.hp = 50 * stage
        self.atk = 100 * stage
        self.attack_time = 0
        self.arrow_x = self.x
        self.arrow_y = self.y
        self.arrow_up = True
        self.arrow_attack = False
        self.arrow_frame= 0
        self.dead_time = 0
        self.arrow_attack_frame = 0
    def arrow_animation(self):
        self.arrow_x -= 10
        if self.arrow_attack_frame < 8:
            self.arrow_attack_frame = self.arrow_attack_frame+1
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
            self.arrow_y +=8
        else:
            self.arrow_y -= 8
        if self.arrow_up and self.arrow_y >= 200:
            self.arrow_up = False
        for object in team:
            if object.x+20+(object.num*20)>=self.arrow_x-40 and object.x-20+(object.num*20)<= self.arrow_x-40 and self.arrow_y <=110:
                object.hp -= self.atk
                self.arrow_attack = False
                self.arrow_x = 900
                self.arrow_y = 700
                self.arrow_up = True
                self.attack_time = 0
                self.arrow_attack_frame = 0
        if self.arrow_y<=82:
            self.arrow_attack = False
            self.arrow_x = 900
            self.arrow_y = 700
            self.arrow_up = True
            self.arrow_attack_frame = 0

    def update(self):
        global enemy_count, go,attack,object,team,pever

        self.attack_time += 1
        if pever==1 and self.atk != 10:
            self.atk = 10
            self.hp = 50
        if go:
                self.x -= 10
                if self.arrow_attack == True:
                    self.arrow_animation()
        if self.hp <= 0:
            self.dead_time+=1
            self.arrow_frame = 0
            self.arrow_x = 900
            self.arrow_y = 700
            self.arrow_up = True
            self.attack_time = 0
            self.arrow_attack = False
            if self.dead_time>=6:
                self.x=800
                self.hp = 100
                self.dead_time=0
        if self.arrow_attack == True:
                self.arrow_animation()
        if self.x > 500:
            self.x -= 10
            self.frame = (self.frame +1) % 10
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
        if self.arrow_attack:
            self.arrow_image.clip_draw(self.arrow_frame*80,0,80,80,self.arrow_x,self.arrow_y)
            self.attack_image.clip_draw(self.arrow_attack_frame*50,0,50,72,self.x,self.y)
        elif self.hp<=0:
            self.dead_image.clip_draw(self.dead_time*48,0,48,72,self.x,self.y)
        else:
            self.image.clip_draw(self.frame*45,0,45,72,self.x,self.y)


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
        self.x, self.y = 900, 89
        self.frame = 0
        self.image = load_image('knight_moving.png')
        self.attack_image = load_image('knight_attack.png')
        self.dead_image = load_image('knight_dead.png')
        self.hp = 100 * stage
        self.atk = 100 * stage
        self.attack_time = 0
        self.attack_frame = 0
        self.attack_check = False
        self.dead_frame = 0
    def knight_attack(self):
        self.attack_frame += 1
        if self.attack_frame>=11:
            self.attack_check = False
            self.attack_frame = 0
    def update(self):
        global enemy_count, go,attack,object,team,pever
        self.frame = (self.frame +1) % 8
        self.attack_time += 1
        if pever==1 and self.atk != 10:
            self.atk = 10
            self.hp = 50
        if go:
                self.x -= 10
        if self.hp <= 0:
            self.dead_frame+=1
            self.attack_time = 0
            if self.dead_frame>=8:
                self.hp = 100
                self.dead_frame = 0
                self.x = 800
        if self.x == 300:
            enemy_count+=1
        if self.x > 250:
            self.x -= 10
        else:
            self.attack_time += 1
            if self.attack_time >= 40:
                self.attack_time = 0
            if self.attack_check:
                self.knight_attack()
            if self.x<=250:
                go = False
                self.frame = 0
                for object in team:
                    if object.num == 2:
                        if attack:
                            self.hp -= object.atk
                            attack = False
                        if self.attack_time >= 30:
                            object.hp -= self.atk
                            self.attack_time = 0
                            self.attack_check = True

    def draw(self):
        if self.attack_check:
            self.attack_image.clip_draw(self.attack_frame*108,0,108,88,self.x,self.y)
        elif self.hp<=0:
            self.dead_image.clip_draw(self.dead_frame*96,0,96,88,self.x,self.y)
        else:
            self.image.clip_draw(self.frame*64,0,64,88,self.x,self.y)


class Object:
    def __init__(self):
        self.x, self.y = 100, 70
        self.frame = 0
        self.num = None
        self.image = load_image('player_character.png')
        self.attack_image = load_image('player_attack_animation.png')
        self.attack_frame = 0
        self.player_attack = False
        self.hp = 100
        self.atk = 10
    def update(self):
        global pever
        if self.player_attack:
            self.attack_animation()
        if pever==1 and self.atk != 50:
            self.atk = 50
            self.hp = 200
            self.y=70
        if attack:
            self.frame = 0
            self.attack_frame = 0
            self.player_attack = True
        if self.hp <= 0:
            self.y += 100
            self.hp = 100
        if go:
            self.frame = (self.frame +1) % 6
        if self.num == 2 and pever == 0:
            self.atk = 20
    def attack_animation(self):
        self.attack_frame += 1
        if self.attack_frame >= 5:
            self.player_attack = False
            self.attack_frame = 0
    def draw(self):
        if self.player_attack:
            self.attack_image.clip_draw(self.attack_frame*80,0,80,45,self.x+50*self.num,self.y)
        else:
            self.image.clip_draw(self.frame*40,0,40,46,self.x+50*self.num,self.y)

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
        elif event.type == SDL_KEYUP and event.key == SDLK_z:
            attack = False

attack = False
num=0
stage=1
enemy_count=1
team = None
game_time = None
go = None
object = None
enemy = None
enemy_army = None
map=None
enemy_arrow = None
grass1 = None
grass2 = None
pever_time = None
pever = None
running = True

def enter():
    global map, grass1,grass2, team,num,go,enemy,stage,enemy_army,enemy_arrow,pever_time,pever, game_time
    open_canvas()
    team = [Object() for i in range(3)]
    enemy_army = [Enemy() for j in range(3)]
    go = False
    game_time = 100
    pever_time = Pever_Time()
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
    global map,boy, grass1,grass2, team,object,enemy,enemy_army,stage,enemy_count,enemy_arrow,pever_time
    del(object)
    del(enemy_count)
    del(grass1)
    del(grass2)
    del(team)
    del(enemy)
    del(map)
    del(stage)
    del(pever_time)
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
    pever_time.draw()

    update_canvas()


def main():
    enter()
    while running:
        handle_events()
        update()
        draw()
        delay(0.06)
    exit()

if __name__ == '__main__':
    main()