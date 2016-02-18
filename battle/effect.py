import pygame
import lib
from copy import copy
from util import get_file_path

NORMAL_DAMAGE = (31, 33)
CRITICAL_DAMAGE = (37, 38)


class Effect:
    def __init__(self):
        self._image = pygame.image.load(
            get_file_path('img/ui/damage.png')).convert_alpha()
        self.damage_images = {
            'normal': [self._image.subsurface(
                (i*NORMAL_DAMAGE[0], 0), NORMAL_DAMAGE) for i in range(10)],
            'critical': [self._image.subsurface(
                (i*CRITICAL_DAMAGE[0], NORMAL_DAMAGE[1]),
                CRITICAL_DAMAGE) for i in range(10)]}
        self.damage_objects = []

    def new_damage(self, number, center, is_critical=False):
        _damage_obj = {
            'number': number,
            'image': self._create_image(number, is_critical),
            'now_center': [center[0], center[1]],
            'origin_center': (center[0], center[1])}
        _damage_obj['image_size'] = _damage_obj['image'].get_size()
        self.damage_objects.append(_damage_obj)

    def render(self):
        _objects = copy(self.damage_objects)
        for obj in _objects:
            obj['now_center'][1] -= lib.data.frame_time / 1000 * 25
            _x = obj['now_center'][0]-obj['image_size'][0]/2
            _y = obj['now_center'][1]-obj['image_size'][1]/2
            lib.draw.draw_image(obj['image'], (_x, _y))
            if obj['now_center'][1]+obj['image_size'][1]/3 <=\
                    obj['origin_center'][1]:
                self.damage_objects.remove(obj)

    def init(self):
        self.damage_objects = []

    def _create_image(self, number, is_critical):
        _type = 'critical' if is_critical else 'normal'
        _str_num = str(number)
        _cell_w, _cell_h = CRITICAL_DAMAGE if is_critical else NORMAL_DAMAGE
        _blanking = int(_cell_w * 0.65)
        _img_w, _img_h = _cell_w+_blanking*(len(_str_num)-1), _cell_h+3
        image = pygame.Surface((_img_w, _img_h), flags=pygame.locals.SRCALPHA)
        for _i, _n in enumerate(_str_num):
            y = 3 if _i % 2 != 0 else 0
            image.blit(self.damage_images[_type][int(_n)], (_i*_blanking, y))
        return image
