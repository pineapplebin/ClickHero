import pygame


class Data:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.frame_time = self.clock.tick(30)
        self.is_loading_done = False
        self.loading_stagename = ''

    def clock_tick(self, framerate=30):
        self.frame_time = self.clock.tick(framerate)
