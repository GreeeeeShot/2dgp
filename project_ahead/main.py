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

class Object:
    def __init__(self):
        self.go = random.randint(1,2)
        self.x, self.y = 100, 100
        self.frame = 0
        self.num = None
        self.image = load_image('run_animation.png')
    def update(self):
        self.frame = (self.frame +1) % 8
    def draw(self):
        self.image.clip_draw(self.frame*100,0,100,100,self.x+50*self.num,self.y)

def handle_events():
    global running, go
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

num=0
team = None
go = None
object = None
grass1 = None
grass2 = None
running = True

def enter():
    global grass1,grass2, team,num,go
    open_canvas()
    team = [Object() for i in range(3)]
    go = False
    grass1 = Grass()
    grass2 = Grass()
    grass1.num = 0
    grass2.num = 1
    for object in team:
        object.num=num
        num += 1

def exit():
    global boy, grass1,grass2, team
    del(object)
    del(grass1)
    del(grass2)
    del(team)
    close_canvas()

def update():
    grass1.update()
    grass2.update()
    for object in team:
        object.update()

def draw():
    clear_canvas()
    grass1.draw()
    grass2.draw()
    for object in team:
        object.draw()
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