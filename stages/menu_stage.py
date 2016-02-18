import pygame
import lib
from pygame.locals import *
from stages.base_stage import BaseStage


class MenuStage(BaseStage):
    def __init__(self):
        BaseStage.__init__(self)
        self.test = pygame.Surface((100, 100))
        self.test_rect = self.test.get_rect()
        self.test_rect.topleft = (100, 100)

    def update(self):
        BaseStage.update(self)
        lib.draw.draw_image(self.test, (100, 100))
        if lib.event.mouse_unpressed and\
                self.test_rect.collidepoint(lib.event.mouse_pos):
            lib.event.post_newstage(
                {'stagename': 'battle', 'initargs': {'mapname': 'map0001'}})
