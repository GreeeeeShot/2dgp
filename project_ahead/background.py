import random

from pico2d import *


class Background:
    PIXEL_PER_METER = (10.0 / 0.3)           # 10 pixel 30 cm
    SCROLL_SPEED_KMPH = 20.0                    # Km / Hour
    SCROLL_SPEED_MPM = (SCROLL_SPEED_KMPH * 1000.0 / 60.0)
    SCROLL_SPEED_MPS = (SCROLL_SPEED_MPM / 60.0)
    SCROLL_SPEED_PPS = (SCROLL_SPEED_MPS * PIXEL_PER_METER)
    SCROLL_SPEED_PPS_1 = (SCROLL_SPEED_MPS * PIXEL_PER_METER)

    def __init__(self, w, h):
        self.image1 = load_image('./image/background.png') # 960x272
        self.image2 = load_image('./image/background2.png')
        self.image3 = load_image('./image/background3.png')
        self.image4 = load_image('./image/background4.png')
        self.bgm1 = load_music('./bgm/bgm1.ogg')
        self.bgm2 = load_music('./bgm/bgm2.ogg')
        self.bgm3 = load_music('./bgm/bgm3.ogg')
        self.bgm4 = load_music('./bgm/bgm4.ogg')
        self.speed = 0
        self.left = 0
        self.screen_width = w
        self.screen_height = h
        self.bgm1.set_volume(64)
        self.bgm1.repeat_play()

    def draw(self,stage):
        x=int(self.left)
        if stage == 1:
            w = min(self.image1.w - x, self.screen_width)
            self.image1.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
            self.image1.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

        elif stage == 2:
            w = min(self.image2.w - x, self.screen_width)
            self.image2.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
            self.image2.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

        elif stage == 3:
            w = min(self.image3.w - x, self.screen_width)
            self.image3.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
            self.image3.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

        elif stage == 4:
            w = min(self.image4.w - x, self.screen_width)
            self.image4.clip_draw_to_origin(x,0,w,self.screen_height,0,0)
            self.image4.clip_draw_to_origin(0,0,self.screen_width-w,self.screen_height,w,0)

    def update(self, frame_time):
        self.left = (self.left + frame_time * self.speed) % self.image1.w

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.speed += Background.SCROLL_SPEED_PPS
            elif event.key == SDLK_z:
                if self.speed>0:
                    self.speed -= Background.SCROLL_SPEED_PPS
        if event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                if self.speed>0:
                    self.speed -= Background.SCROLL_SPEED_PPS