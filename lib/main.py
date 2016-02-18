import pygame
import threading
import lib
from stages import StageFactory
from lib.constant import *


class StageManager:
    """
    场景管理类,用于切换stage
    """
    def __init__(self):
        self.stages = {}
        self.curr_stagename = ''
        self.stage_factory = StageFactory()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Click Maple Story')

    def update(self):
        lib.data.clock_tick()
        new_stage = lib.event.get()
        if new_stage:
            if new_stage['change_type'] == E_NEWSTAGE:
                self.change_stage(new_stage)
            elif new_stage['change_type'] == E_LOADINGDONE:
                self.curr_stagename = new_stage['stagename']
        self.stages[self.curr_stagename].update()
        lib.draw.draw_mouse()
        pygame.display.update()

    def create_stage(self, stagename):
        self.stages[stagename] = self.stage_factory.create(stagename)

    def change_stage(self, new_stage):
        stagename = new_stage['stagename']
        if stagename not in self.stages:
            self.create_stage(stagename)
        if self.curr_stagename != stagename:
            if self.curr_stagename:
                self.stages[self.curr_stagename].exit()
            self.curr_stagename = 'loading'
            self.loading(stagename, new_stage['initargs'])

    def loading(self, stagename, initargs):
        func = self._decorator(
            self.stages[stagename].init, stagename, initargs)
        t = threading.Thread(target=func, args=(initargs, ))
        t.setDaemon(True)
        t.start()

    def _decorator(self, func, stagename, initargs):
        def _wrapper(initargs):
            lib.data.loading_stagename = stagename
            func(initargs)
            lib.data.is_loading_done = True
        return _wrapper

stage_manager = StageManager()


def run():
    stage_manager.create_stage('menu')
    stage_manager.create_stage('loading')
    lib.event.post_loadingdone({'stagename': 'menu'})
    while True:
        stage_manager.update()
