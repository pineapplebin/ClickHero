import pygame
import lib
from pygame.locals import *
from view.base_controller import BaseController
from view.base_stage import BaseStageView


class MenuStageView(BaseStageView):
    def __init__(self):
        BaseStageView.__init__(self)
        self.controller = MenuStageController(self)
        self.button_image = pygame.Surface((100, 100))
        self.button_rect = self.button_image.get_rect(topleft=(100, 100))

    def render(self):
        BaseStageView.render(self)
        lib.draw.draw_image(self.button_image, (100, 100))
        if lib.event.mouse_unpressed:
            if self.button_rect.collidepoint(lib.event.mouse_pos):
                self.controller.click_start()


class MenuStageController(BaseController):
    def click_start(self):
        lib.event.post_newstage(
            {'stagename': 'battle', 'initargs': {'mapname': 'map0001'}})
