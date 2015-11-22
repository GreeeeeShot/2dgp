from pico2d import *

import game_framework


from unit import Unit # import Boy class from boy.py
from background import Background
from enemy import Enemy_Knight
from collision import collide


name = "scroll_state"

unit = None
background = None
enemy_knight = None
unit_attack = False

def create_world():
    global unit, background,enemy_knight
    unit = Unit()
    background = Background(800, 400)
    enemy_knight = Enemy_Knight()


def destroy_world():
    global unit, background,enemy_knight
    del(unit)
    del(background)
    del(enemy_knight)


def enter():
    open_canvas(800, 400)
    game_framework.reset_time()
    create_world()


def exit():
    destroy_world()
    close_canvas()


def pause():
    pass

def resume():
    pass


def handle_events(frame_time):
    global unit_attack
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                unit.handle_event(event)
                background.handle_event(event)
                if not collide(enemy_knight,unit):
                    enemy_knight.handle_event(event)



def update(frame_time):
    enemy_knight.update(frame_time)
    unit.update(frame_time)
    background.update(frame_time)
    if collide(enemy_knight,unit):
        if unit.state == unit.RUN:
            unit.state = unit.STAND
        if enemy_knight.state == enemy_knight.RUN:
            enemy_knight.state = enemy_knight.STAND
        background.speed = 0
        unit.attack_damage(enemy_knight)
        enemy_knight.speed=0





def draw(frame_time):
    clear_canvas()
    background.draw()
    unit.draw()
    enemy_knight.draw()
    unit_attack = False
    update_canvas()

