import pygame
import sys
from pygame.locals import *
from lib.constant import *


class Event:
    def __init__(self):
        self.mouse_clicked = False
        self.mouse_pressed = False
        self.mouse_unpressed = False
        self.mouse_pos = [0, 0]

    def get(self):
        self.mouse_unpressed = False
        new_stage = {}
        for e in pygame.event.get():
            if e.type == MOUSEMOTION:
                self.mouse_pos = list(e.pos)
            elif e.type == MOUSEBUTTONDOWN:
                self.clicked = True
                self.mouse_pressed = e.button
                self.mouse_unpressed = False
            elif e.type == MOUSEBUTTONUP:
                self.clicked = False
                self.mouse_unpressed = e.button
                self.mouse_pressed = False
            elif e.type == USEREVENT:
                new_stage['change_type'] = e.change_type
                new_stage['stagename'] = e.stagename
                if hasattr(e, 'initargs'):
                    new_stage['initargs'] = e.initargs
            elif e.type == QUIT:
                pygame.event.post(e)
        self.check_quit()
        return new_stage

    def check_quit(self):
        for event in pygame.event.get(QUIT):
            self.terminate()

    def terminate(self):
        pygame.display.quit()
        sys.exit()

    def post_newstage(self, message):
        if not isinstance(message, dict):
            raise TypeError('message must be dict type')
        message['change_type'] = E_NEWSTAGE
        e = pygame.event.Event(USEREVENT, message)
        pygame.event.post(e)

    def post_loadingdone(self, message):
        if not isinstance(message, dict):
            raise TypeError('message must be dict type')
        message['change_type'] = E_LOADINGDONE
        e = pygame.event.Event(USEREVENT, message)
        pygame.event.post(e)
