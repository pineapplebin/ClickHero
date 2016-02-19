import pygame
import lib
from copy import copy
from util import get_file_path
from util.iqueue import IQueue

NORMAL_DAMAGE = (31, 33)
CRITICAL_DAMAGE = (37, 38)
MAX_DAMAGE_COUNT = 50


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
        self.damage_queue = IQueue(MAX_DAMAGE_COUNT)
        self.passed_time_second = 0

    def render(self):
        self.passed_time_second += lib.data.get_passed_second()
        pop_count = 0
        for obj in self.damage_queue:
            if obj['start_time'] < self.passed_time_second - 0.6:
                pop_count += 1
            if obj['start_time'] > self.passed_time_second:
                continue
            obj['center'][1] -= lib.data.frame_time / 1000 * 25
            _x = obj['center'][0]-obj['image_size'][0]/2
            _y = obj['center'][1]-obj['image_size'][1]/2
            lib.draw.draw_image(obj['image'], (_x, _y))
        [self.damage_queue.pop() for i in range(pop_count)]

    def new_damage(self, damage_or_list, center_point):
        self._new_damage_list(damage_or_list, center_point)

    def init(self):
        self.passed_time_second = 0
        self.damage_queue = IQueue(MAX_DAMAGE_COUNT)

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

    def _new_damage_list(self, damage_list, center):
        # damage[0] is number, [1] is is_critical
        blanking = 0
        for damage in damage_list:
            _image = self._create_image(damage[0], damage[1])
            _damage_obj = {
                'start_time': self.passed_time_second + blanking * 0.1,
                'number': damage[0],
                'image': _image,
                'center': [center[0]+blanking*5, center[1]-blanking*25],
                'image_size': _image.get_size()}
            if self.damage_queue.is_full():
                self.damage_queue.pop()
            self.damage_queue.put(_damage_obj)
            blanking += 1
