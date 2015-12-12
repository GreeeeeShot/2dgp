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
        self.image = 0
        if Morale.fail_image == None:
            Morale.fail_image = load_image("./image/fail.png")
        if Morale.success_image == None:
            Morale.success_image = load_image("./image/pever.png")

    def morale_success(self,unit):
        unit.hp = 50000
        unit.atk = 50
        unit.first_hp = 50000
        self.image = Morale.SUCCESS
        self.state = Morale.CHALLINGE

    def morale_fail(self,unit):
        unit.atk = 5
        self.image = Morale.FAIL
        self.state = Morale.CHALLINGE

    def draw(self):
        if self.image == Morale.FAIL:
            self.fail_image.clip_draw(20,100,400,200,400,200)
        elif self.image == Morale.SUCCESS:
            self.success_image.clip_draw(20,100,400,200,400,200)