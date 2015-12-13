import game_framework
import main_state
from pico2d import *


name = "TitleState"
image = None
bgm = None

def enter():
    global image, bgm
    image = load_image('./image/title.png')
    bgm = load_music('./bgm/titlebgm.ogg')
    bgm.set_volume(128)
    bgm.repeat_play()


def exit():
    global image
    del(image)


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw(frame_time):
    clear_canvas()
    image.draw(400,200)
    update_canvas()







def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass






