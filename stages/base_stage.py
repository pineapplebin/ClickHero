import lib
from lib.constant import *


class BaseStage:
    def __init__(self):
        self.background_color = C_WHITE

    def update(self):
        lib.draw.fill_color(self.background_color)

    def init(self, initargs=None):
        pass

    def exit(self):
        pass
