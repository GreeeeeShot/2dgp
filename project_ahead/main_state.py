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
from stage_view import Stage_View

name = "main_state"

unit = None
background = None
enemy_knight = None
enemy_archur = None
arrow1 = None
arrow2 = None
unit_attack = False
morale = None
ingame_time = None
mini_map = None
count_killed = None
stage_view = None

def create_world():
    global unit, background,enemy_knight,enemy_archur,arrow1,arrow2,morale,ingame_time,mini_map,count_killed,stage_view
    unit = Unit()
    stage_view = Stage_View()
    background = Background(800, 400)
    enemy_knight = Enemy_Knight()
    enemy_archur = Enemy_Archur()
    arrow1 = Arrow()
    arrow2 = Arrow()
    morale = Morale()
    ingame_time = Ingame_Time()
    mini_map = Mini_Map()
    count_killed = Count_Killed()

def destroy_world():
    global unit, background,enemy_knight,enemy_archur,arrow1,arrow2,morale,ingame_time,mini_map,count_killed,stage_view
    del(unit)
    del(stage_view)
    del(morale)
    del(count_killed)
    del(arrow1)
    del(arrow2)
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
        if enemy_archur.state in (enemy_archur.STAND,enemy_archur.ATTACK1,enemy_archur.ATTACK2):
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
    if enemy_knight.update(frame_time,mini_map.stage):
        count_killed.count()
    if enemy_archur.update(frame_time,mini_map.stage):
        count_killed.count()
    background.update(frame_time)
    unit.update(frame_time,mini_map.stage)

    arrow1.update(frame_time)

    if enemy_archur.state == Enemy_Archur.ATTACK1:
        arrow1.state = Arrow.ATTACK
        arrow1.x=enemy_archur.x
        arrow1.y=enemy_archur.y
        arrow1.draw_frame = 0
        arrow1.arrow_up = True
    if collide(arrow1,unit):
        arrow1.state = arrow1.REST
        enemy_archur.attack_damage(unit)

    arrow2.update(frame_time)
    if enemy_archur.state == Enemy_Archur.ATTACK2:
        arrow2.state = Arrow.ATTACK
        arrow2.x=enemy_archur.x
        arrow2.y=enemy_archur.y
        arrow2.draw_frame = 0
        arrow2.arrow_up = True
    if collide(arrow2,unit):
        arrow2.state = arrow2.REST
        enemy_archur.attack_damage(unit)

    ingame_time.update(frame_time,morale)
    mini_map.update(frame_time,morale,ingame_time)
    if (morale.state == morale.FAIL) and (morale.image != morale.SUCCESS):
        morale.morale_fail(unit)
    if (morale.state == morale.SUCCESS) and (morale.image != morale.FAIL):
        morale.morale_success(unit)

    if mini_map.position_x>=680 and mini_map.stage<4:
        mini_map.stage += 1
        enemy_knight.atk = mini_map.stage*1
        enemy_knight.hp = (mini_map.stage-1)*5000+3000
        enemy_archur.atk = mini_map.stage*1
        enemy_archur.hp = (mini_map.stage-1)*5000+3000
        morale.image = 0
        unit.atk = mini_map.stage * 5+ 5
        unit.hp = mini_map.stage * 35000
        unit.first_hp = unit.hp
        mini_map.position_x = 120
        mini_map.position_y = 320
        mini_map.state = Mini_Map.STAND
        mini_map.speed = 0
        mini_map.total_frames = 0.0
        enemy_knight.x, enemy_knight.y = 700, 70
        enemy_archur.x, enemy_archur.y = 700, 70
        stage_view.total_frame = 0.0
        ingame_time.start_time = -1.0
        ingame_time.total_frames = 0.0
        if mini_map.stage == 2:
            ingame_time.stage = Ingame_Time.STAGE2
            background.bgm1.stop()
            background.bgm2.set_volume(64)
            background.bgm2.repeat_play()
        if mini_map.stage == 3:
            ingame_time.stage = Ingame_Time.STAGE3
            background.bgm2.stop()
            background.bgm3.set_volume(64)
            background.bgm3.repeat_play()
        if mini_map.stage == 4:
            ingame_time.stage = Ingame_Time.STAGE4
            background.bgm3.stop()
            background.bgm4.set_volume(64)
            background.bgm4.repeat_play()
        ingame_time.run_time = True
        background.speed = 0
        background.left = 0
        background.screen_width = 800
        background.screen_height = 400
        enemy_knight.first_hp = enemy_knight.hp
        enemy_archur.first_hp = enemy_archur.hp





def draw(frame_time):
    clear_canvas()
    background.draw(mini_map.stage)
    morale.draw()
    unit.draw()
    enemy_knight.draw()
    enemy_archur.draw()
    arrow1.draw()
    arrow2.draw()
    ingame_time.draw()
    mini_map.draw()
    count_killed.draw()
    stage_view.draw(frame_time,mini_map.stage)
    update_canvas()


