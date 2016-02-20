import pygame
import lib
from model import BaseModel
from pygame.sprite import Sprite, Group
from util import get_file_path
from util.vector2 import Vector2
from random import randint
from lib.constant import *

_rate = 150
TYPE_MONEY = 0
TYPE_ITEM = 1
ITEM_RARE_SIZE = (42, 44)


class ItemGroupModel(Group, BaseModel):
    def __init__(self):
        Group.__init__(self)
        BaseModel.__init__(self)
        # load image
        _money_image = pygame.image.load(
            get_file_path('img/item/money.png')).convert_alpha()
        _subsurface_data = [(25, 24), (25, 24), (33, 30), (32, 31)]
        _y = 0
        self.money_images = []
        for _sub_data in _subsurface_data:
            _tmp_list = [_money_image.subsurface(
                (i*_sub_data[0], _y), _sub_data) for i in range(4)]
            _y += _sub_data[1]
            self.money_images.append(_tmp_list)
        _item_rare_image = pygame.image.load(
            get_file_path('img/item/rare_42x44.png')).convert_alpha()
        self.item_rare_images = [_item_rare_image.subsurface(
            (i*ITEM_RARE_SIZE[0], 0), ITEM_RARE_SIZE) for i in range(6)]
        # load icons, but now only load one image
        self.item_icons = pygame.image.load(
            get_file_path('img/item/04000019.png')).convert_alpha()

    def render(self):
        for item in self.sprites():
            item.render()

    def get_render_data(self):
        data_list = []
        for item in self.sprites():
            item.update()
            data_list.append((item.image, item.get_pos('topleft')))
        return data_list

    def collide(self, pos):
        for item in self.sprites():
            item.collide(pos)

    def drop_money(self, money, center):
        if money < 100:
            i = 0
        elif money >= 100 and money < 1000:
            i = 1
        elif money >= 1000 and money < 10000:
            i = 2
        elif money >= 10000:
            i = 3
        self.add(DropSprite(money, center, self.money_images[i], TYPE_MONEY))

    def drop_item(self, item_id, center):
        item = item_id[:-2]
        rare = int(item_id[-1])
        item_image = pygame.Surface(
            ITEM_RARE_SIZE, flags=pygame.locals.SRCALPHA)
        item_image.blit(self.item_rare_images[rare], (0, 0))
        _w, _h = self.item_icons.get_size()
        item_image.blit(self.item_icons, (
            (ITEM_RARE_SIZE[0]-_w)/2, (ITEM_RARE_SIZE[1]-_h)/2))
        item_image.blit(self.item_rare_images[0], (0, 0))
        self.add(DropSprite(item, center, item_image, TYPE_ITEM))


class DropSprite(Sprite):
    def __init__(self, money_or_id, center, images_or_image, drop_type):
        Sprite.__init__(self)
        self.type = drop_type
        if drop_type == TYPE_MONEY:
            self.images = images_or_image
            self.image = self.images[0]
            self.money = money_or_id
        else:
            self.image = images_or_image
            self.item_id = money_or_id
        self.rect = self.image.get_rect(center=center)
        self.center = Vector2((center[0], center[1]-15))
        self.w, self.h = self.image.get_size()
        self.set_destination((0, 0))
        self.speed = 10
        self.passed_time = 0
        self.states = {}
        self.active_state = None
        self.add_state(AppearState(self))
        self.add_state(WaitState(self))
        self.add_state(FlyState(self))
        self.set_state('appear')
        self.bag_pos = (950, 630)
        self.is_flying = False

    def update(self):
        self.passed_time += lib.data.frame_time
        self.think()

    def render(self):
        self.update()

    def move(self):
        if self.type == TYPE_MONEY:
            img_index = int(self.passed_time / _rate) % 4
            self.image = self.images[img_index]
        self.center += self.vector_to_destination * self.speed
        self.rect = self.image.get_rect(center=self.center)
        x, y = self.center[0]-self.w/2, self.center[1]-self.h/2
        # self.topleft = (x, y)
        lib.draw.draw_image(self.image, (x, y))

    def set_destination(self, x_or_pair, y=None):
        if y is None:
            self.destination = Vector2(x_or_pair)
        else:
            self.destination = Vector2(x_or_pair, y)
        self.vector_to_destination = Vector2.from_points(
            self.center, self.destination).normalized()

    def collide(self, pos):
        if self.is_flying:
            return
        if self.rect.collidepoint(pos):
            self.set_state('fly')

    def get_pos(self, point='center'):
        if not self.image:
            return None
        _w, _h = self.image.get_size()
        if point == 'center':
            return self.center[0], self.center[1]
        elif point == 'topleft':
            return self.center[0]-_w/2, self.center[1]-_h/2

    # state machine
    def add_state(self, state):
        self.states[state.name] = state

    def think(self):
        if not self.active_state:
            return
        self.active_state.do_action()
        self.active_state.check_condition()
        if self.active_state.next_state:
            self.set_state(self.active_state.next_state)

    def set_state(self, new_state_name):
        if self.active_state:
            self.active_state.exit_action()
        self.active_state = self.states[new_state_name]
        self.active_state.entry_action()


class State:
    def __init__(self, state_name):
        self.name = state_name
        self.next_state = ''

    def entry_action(self):
        self.sprite.passed_time = 0
        self.next_state = ''
        self.origin_y = self.sprite.center[1]

    def do_action(self):
        self.sprite.move()

    def check_condition(self):
        pass

    def exit_action(self):
        pass


class AppearState(State):
    def __init__(self, sprite):
        State.__init__(self, 'appear')
        self.sprite = sprite

    def entry_action(self):
        State.entry_action(self)
        self.offset_y = -50
        self.offset_x = randint(-25, 25)
        x = self.sprite.center[0] + self.offset_x
        y = self.sprite.center[1] + self.offset_y
        self.sprite.set_destination(x, y)
        self.direction = -1
        self.check_border = False

    def check_condition(self):
        if not self.check_border:
            if self.sprite.center[0]-self.sprite.w/2 < 0 or\
                    self.sprite.center[0]+self.sprite.w/2 > SCREEN_SIZE[0]:
                self.sprite.set_destination(
                    self.sprite.center[0], self.origin_y)
                self.direction = 1
                self.check_border = True
        if self.direction*self.sprite.center[1] >\
                self.direction*self.sprite.destination[1]:
            if self.direction < 0:
                self.sprite.set_destination(
                    self.sprite.center[0]+self.offset_x, self.origin_y)
                self.direction = 1
            else:
                self.next_state = 'wait'


class WaitState(State):
    def __init__(self, sprite):
        State.__init__(self, 'wait')
        self.sprite = sprite

    def entry_action(self):
        State.entry_action(self)
        self.sprite.speed = 1
        self.offset_y = 10
        self.sprite.set_destination(
            self.sprite.center[0],
            self.sprite.destination[1]+self.offset_y)
        self.direction = 1

    def check_condition(self):
        if self.sprite.passed_time > 30000:
            self.sprite.kill()
            return
        if self.direction*self.sprite.center[1] >\
                self.direction*self.sprite.destination[1]:
            self.direction *= -1
            self.offset_y *= -1
            self.sprite.set_destination(
                self.sprite.center[0],
                self.sprite.center[1]+self.offset_y)


class FlyState(State):
    def __init__(self, sprite):
        State.__init__(self, 'fly')
        self.sprite = sprite
        self.passed_time = 0

    def entry_action(self):
        State.entry_action(self)
        self.sprite.set_destination(self.sprite.bag_pos)
        self.sprite.is_flying = True
        self.sprite.speed = 15

    def check_condition(self):
        if self.sprite.center[1] > self.sprite.bag_pos[1]:
            self.sprite.kill()
