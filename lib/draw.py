import pygame
import lib
from util import get_file_path
from lib.constant import *


class Draw:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        self.cursors = [
            pygame.image.load(
                get_file_path('img/ui/cursor.png')).convert_alpha(),
            pygame.image.load(
                get_file_path('img/ui/cursor_click.png')).convert_alpha()]

    def draw_mouse(self):
        cursor = 1 if lib.event.mouse_pressed else 0
        self.screen.blit(self.cursors[cursor], lib.event.mouse_pos)

    def fill_color(self, color):
        self.screen.fill(color)

    def draw_image(self, surface, pos):
        self.screen.blit(surface, pos)

    def fill(self, color, rect):
        self.screen.fill(color, rect)
