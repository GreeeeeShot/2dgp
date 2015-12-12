__author__ = 'Administrator'
from pico2d import *

class Stage_View:
    def __init__(self):
        self.font = load_font('ConsolaMalgun.ttf',40)
        self.total_frame = 0.0


    def draw(self,frame_time,stage,unit):
        print("%f"% frame_time)
        self.total_frame+=frame_time
        if self.total_frame < 2:
            self.font.draw(340,250,"Stage %d" % stage)
        if unit.state==unit.DEAD:
            self.font.draw(300,200,"Game Over")

def test_stage_view():
    open_canvas()
    stage_view = Stage_View()
    stage_view.draw(5)
    update_canvas()
    close_canvas()

if __name__ == '__main__':
    test_stage_view()
