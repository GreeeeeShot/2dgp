from pico2d import *

import game_framework


from unit import Unit # import Boy class from boy.py
from background import Background
from enemy import Enemy_Knight
from collision import collide
from enemy import Enemy_Archur
from enemy import Arrow
from morale import Morale
from ingame_time import Ingame_Time
from mini_map import Mini_Map
from count_killed import Count_Killed

name = "main_state"

unit = None
background = None
enemy_knight = None
enemy_archur = None
arrow = None
unit_attack = False
morale = None
ingame_time = None
mini_map = None
count_killed = None

def create_world():
    global unit, background,enemy_knight,enemy_archur,arrow,morale,ingame_time,mini_map,count_killed
    unit = Unit()
    background = Background(800, 400)
    enemy_knight = Enemy_Knight()
    enemy_archur = Enemy_Archur()
    arrow = Arrow()
    morale = Morale()
    ingame_time = Ingame_Time()
    mini_map = Mini_Map()
    count_killed = Count_Killed()

def destroy_world():
    global unit, background,enemy_knight,enemy_archur,arrow,morale,ingame_time,mini_map,count_killed
    del(unit)
    del(morale)
    del(count_killed)
    del(arrow)
    del(ingame_time)
    del(background)
    del(enemy_knight)
    del(enemy_archur)
    del(mini_map)


def enter():
    #open_canvas(800, 400)
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
                if ((event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT)) and mini_map.position_x>=680:
                    game_framework.quit()
                unit.handle_event(event)
                mini_map.handle_event(event,unit)
                if not collide(enemy_knight,unit) and not collide(enemy_archur,unit):
                    background.handle_event(event)
                    enemy_knight.handle_event(event)
                    enemy_archur.handle_event(event)


def update(frame_time):
    if collide(enemy_knight,unit):
        if unit.state == unit.RUN:
            unit.state = unit.STAND
        if enemy_knight.state == enemy_knight.RUN:
            enemy_knight.state = enemy_knight.STAND
        if enemy_archur.state in (enemy_archur.STAND,enemy_archur.ATTACK):
            enemy_archur.speed=0
        if mini_map.state == mini_map.RUN:
            mini_map.state = mini_map.STAND
        background.speed = 0
        unit.attack_damage(enemy_knight)
        enemy_knight.speed=0
        if enemy_knight.state == enemy_knight.ATTACK:
            enemy_knight.attack_damage(unit)
    if collide(enemy_archur,unit):
        if unit.state == unit.RUN:
            unit.state = unit.STAND
        if enemy_archur.state == enemy_archur.RUN:
            enemy_archur.state = enemy_archur.STAND
        if mini_map.state == mini_map.RUN:
            mini_map.state = mini_map.STAND
        background.speed = 0
        unit.attack_damage(enemy_archur)
        enemy_archur.speed=0
    elif enemy_archur.x <= 500 and enemy_archur.state == enemy_archur.RUN:
        enemy_archur.state = enemy_archur.STAND
        enemy_archur.speed -= Enemy_Archur.TIME_PER_ACTION
    if enemy_knight.update(frame_time):
        count_killed.count()
    if enemy_archur.update(frame_time):
        count_killed.count()
    background.update(frame_time)
    unit.update(frame_time)
    arrow.update(frame_time)
    if enemy_archur.state == Enemy_Archur.ATTACK:
        arrow.state = Arrow.ATTACK
        arrow.x=enemy_archur.x
        arrow.y=enemy_archur.y
        arrow.draw_frame = 0
        arrow.arrow_up = True
    if collide(arrow,unit):
        arrow.state = arrow.REST
        enemy_archur.attack_damage(unit)
    ingame_time.update(frame_time,morale)
    mini_map.update(frame_time,morale,ingame_time)
    if (morale.state == morale.FAIL) and (morale.image != morale.SUCCEESS):
        morale.morale_fail(unit)
    if (morale.state == morale.SUCCESS) and (morale.image != morale.FAIL):
        morale.morale_success(unit)




def draw(frame_time):
    clear_canvas()
    background.draw()
    morale.draw()
    unit.draw()
    enemy_knight.draw()
    enemy_archur.draw()
    arrow.draw()
    ingame_time.draw()
    mini_map.draw()
    count_killed.draw()
    update_canvas()


