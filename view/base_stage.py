import lib
from lib.constant import *


class BaseStageView:
    def __init__(self):
        self.background_color = C_WHITE

    def render(self):
        lib.draw.fill_color(self.background_color)

    def init(self, initargs=None):
        pass

    def exit(self):
        pass

    def notice(self, model):
        pass
