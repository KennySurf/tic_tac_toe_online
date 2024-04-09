import storage
from game import Game
from lib.renderer import Renderer
from pygame import locals

FADE_SPEED = 0.0015


class Scene:
    def __init__(self):
        self.renderer = Renderer((768, 768), self.calc_stage_size, "white", "black")
        self.game = Game()
        self.stage = None
        self.fade_speed = 0
        self.fade = 1

    def start(self):
        self.fade_to_stage(self.game)

    def fade_to_stage(self, stage):
        self.next_stage = stage
        if self.stage:
            self.fade_speed = -FADE_SPEED
            self.fade = 1
        else:
            self.change_scene()

    def change_scene(self):
        self.stage = self.next_stage
        self.renderer.invalidate_surface_size()
        self.stage.start()

    def mousedown(self, button: int):
        if self.fade_speed >= 0:
            pos = self.renderer.get_mouse()
            self.stage.mousedown(pos, button)

    def keydown(self, key: int):
        match key:
            case locals.K_F2:
                self.renderer.scale_mode = self.renderer.scale_mode.next()
            case locals.K_F3:
                storage.debug = not storage.debug
            case _:
                if self.fade_speed >= 0:
                    self.stage.keydown(key)

    def update(self, tick):
        self.stage.update(tick)
        self.stage.draw(self.renderer.surface)

        if self.fade_speed != 0:
            self.fade += self.fade_speed * tick
            if self.fade <= 0:
                self.fade = 0
                self.fade_speed *= -1
                self.change_scene()
            elif self.fade >= 1:
                self.fade = 1
                self.fade_speed = 0

        self.renderer.render(self.fade)

    def calc_stage_size(self, app_size: tuple[int, int]) -> tuple[int, int]:
        return self.stage.calc_stage_size(app_size)
