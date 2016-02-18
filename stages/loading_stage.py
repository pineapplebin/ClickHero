import pygame
import lib
from stages.base_stage import BaseStage
from lib.constant import C_WHITE, SCREEN_SIZE


class LoadingStage(BaseStage):
    def __init__(self):
        BaseStage.__init__(self)
        self.background_color = (0, 0, 0)
        self.font = pygame.font.SysFont('微软雅黑', 24)
        self.dot_count = 0
        self.passed_time = 0
        self.rate = 500

    def update(self):
        BaseStage.update(self)
        self.passed_time += lib.data.frame_time
        if not lib.data.is_loading_done:
            self.dot_count = int(self.passed_time / self.rate) % 4
            text = '请稍候' + '.'*self.dot_count
        else:
            text = '请点击以继续'
        show = self.font.render(text, True, C_WHITE)
        w, h = show.get_size()
        lib.draw.draw_image(
            show, ((SCREEN_SIZE[0]-w)/2, (SCREEN_SIZE[1]-h)/2))
        if self.passed_time > self.rate and self.dot_count == 0:
            self.passed_time = 0
        self.check_continue_click()

    def check_continue_click(self):
        if lib.data.is_loading_done:
            if lib.event.mouse_unpressed:
                lib.event.post_loadingdone(
                    {'stagename': lib.data.loading_stagename})
                lib.data.is_loading_done = False
                lib.data.loading_stagename = ''
