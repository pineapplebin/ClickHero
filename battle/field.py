import pygame
import lib
from util import get_file_path, randindex
from pygame.locals import SRCALPHA


class Field:
    def __init__(self, fielddata):
        self.footholds = []
        self.footholds_count = 0
        self.background_img = pygame.image.load(
            get_file_path(fielddata['background_img'])).convert()
        self.tiles_img = pygame.image.load(
            get_file_path(fielddata['tiles_img'])).convert_alpha()
        for fh in fielddata['footholds']:
            tmp = {
                'pos': fh['pos'], 'width': fh['size'][0],
                'image': pygame.Surface(fh['size'], SRCALPHA)}
            x = 0
            for t in fh['tiles']:
                repeat, sub_pos, rand_tile = 1, (0, 0), False
                if 'repeat' in t:
                    repeat = t['repeat']
                if isinstance(t['sub_pos'], list):
                    rand_tile = True
                for _ in range(repeat):
                    sub_pos = t['sub_pos'][randindex(len(t['sub_pos']))] if\
                        rand_tile else t['sub_pos']
                    x = self._build_image(tmp['image'], x, sub_pos, t['size'])
            self.footholds.append(tmp)
            self.footholds_count += 1

    def render(self):
        lib.draw.draw_image(self.background_img, (0, 0))
        for fh in self.footholds:
            lib.draw.draw_image(fh['image'], fh['pos'])

    def get_rand_field(self):
        foothold = self.footholds[randindex(self.footholds_count)]
        return (foothold['pos'][0], foothold['pos'][1], foothold['width'])

    def empty(self):
        self.footholds = []
        self.footholds_count = 0
        del self.background_img
        del self.tiles_img

    def _build_image(self, surface, x, sub_pos, sub_size):
        sub_surface = self.tiles_img.subsurface(sub_pos, sub_size)
        surface.blit(sub_surface, (x, 0))
        return x + sub_size[0]
