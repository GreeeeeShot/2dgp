from pico2d import *

class Mini_Map:

    TIME_PER_ACTION = 0.08
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    STAGE1, STAGE2 , STAGE3 , STAGE4 , RUN , STAND = 1, 2 , 3 , 4 , 5 , 6
    stage1_image = None
    stage2_image = None
    stage3_image = None
    stage4_image = None
    position_image = None

    def __init__(self):
        self.stage = Mini_Map.STAGE1
        if Mini_Map.stage1_image == None:
            Mini_Map.stage1_image = load_image("map.png")
        if Mini_Map.stage2_image == None:
            Mini_Map.stage2_image = load_image("map.png")
        if Mini_Map.stage3_image == None:
            Mini_Map.stage3_image = load_image("map.png")
        if Mini_Map.stage4_image == None:
            Mini_Map.stage4_image = load_image("map.png")
        if Mini_Map.position_image == None:
            Mini_Map.position_image = load_image("moving.png")
        self.position_x = 120
        self.position_y = 320
        self.total_frames = 0.0
        self.state = Mini_Map.STAND
        self.speed = 0

    def update(self,frame_time,morale,ingame_time):
        def clamp(minimum, x, maximum):
            return max(minimum, min(x, maximum))
        self.total_frames += Mini_Map.FRAMES_PER_ACTION * Mini_Map.ACTION_PER_TIME * frame_time
        if self.state == Mini_Map.RUN:
            self.position_x += self.speed
        if self.position_x>=500:
            morale.state = morale.SUCCESS
            if ingame_time.run_time :
                ingame_time.stop()


    def draw(self):
        self.stage1_image.clip_draw(0,0,600,100,400,340)
        self.position_image.clip_draw(0,0,22,24,self.position_x,self.position_y)

    def handle_event(self, event, unit):

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            print(self.speed)
            self.state = Mini_Map.RUN
            if self.speed>=0:
                self.speed += Mini_Map.TIME_PER_ACTION
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            if unit.state in (unit.STAND, unit.RUN):
                self.state = Mini_Map.STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            self.state = Mini_Map.STAND
            if self.speed>=Mini_Map.TIME_PER_ACTION:
                self.speed -= Mini_Map.TIME_PER_ACTION
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_z):
            if unit.check_run:
                self.state = Mini_Map.RUN