import random

from pico2d import *

class Morale:
    SUCCESS , FAIL , CHALLINGE = 1 , 2 , 3
    fail_image = None
    success_image=None
    def __init__(self):
        self.enemy_morale = 50
        self.unit_morale = 50
        self.state = Morale.CHALLINGE
        if Morale.fail_image == None:
            Morale.fail_image = load_image("fail.png")
        if Morale.success_image == None:
            Morale.success_image = load_image("pever.png")

    def morale_success(self,unit):
        unit.hp = 500
        unit.atk = 50
        self.state = Morale.SUCCESS

    def morale_fail(self,unit):
        unit.atk = 10
        self.state = Morale.FAIL

    def draw(self):
        if self.state == Morale.FAIL:
            self.fail_image.clip_draw(20,100,400,200,400,200)
        elif self.state == Morale.SUCCESS:
            self.success_image.clip_draw(20,100,400,200,400,200)