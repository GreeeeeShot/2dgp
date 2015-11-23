from pico2d import *

import game_framework


from unit import Unit
from background import Background
from enemy import Enemy_Knight



name = "main_state"

unit = None
background = None
enemy_knight = None

def create_world():
    global unit, background,enemy_knight

    unit = Unit()
    background = Background()
    enemy_knight = Enemy_Knight()


def destroy_world():
    global unit, background,enemy_knight

    del(unit)
    del(background)
    del(enemy_knight)



def enter():
    open_canvas()
    hide_cursor()
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
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            else:
                boy.handle_event(event)



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def update(frame_time):
    unit.update(frame_time)
    enemy_knight.update(frame_time)


def draw(frame_time):
    clear_canvas()
    background.draw()
    unit.draw()
    enemy_knight.draw()

    update_canvas()






