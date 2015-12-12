from pico2d import *

class Ingame_Time:

    TIME_PER_ACTION = 1.0
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8
    num_image = None
    STAGE1 , STAGE2, STAGE3, STAGE4 = 40 , 60 , 80 , 100

    def __init__(self):
        self.start_time = -1.0
        self.total_frames = 0.0
        self.stage = Ingame_Time.STAGE1
        self.run_time = True
        if Ingame_Time.num_image == None:
            Ingame_Time.num_image = load_image("num.png")

    def update(self,frame_time,morale):
        if self.run_time :
            self.total_frames += Ingame_Time.FRAMES_PER_ACTION * Ingame_Time.ACTION_PER_TIME * frame_time
        if self.start_time <= 0:
            self.start_time = self.total_frames
        if int((self.total_frames-self.start_time)/10)>=self.stage:
            morale.state = morale.FAIL
            self.stop()

    def draw(self):
        self.num_image.clip_draw((int((self.stage-(self.total_frames-self.start_time)/10))%10)*16,0,16,32,770,350)
        self.num_image.clip_draw((int((self.stage-(self.total_frames-self.start_time)/10)/10))*16,0,16,32,750,350)
        self.num_image.clip_draw((int((self.stage-(self.total_frames-self.start_time)/100)/100))*16,0,16,32,730,350)

    def stop(self):
        self.run_time = False