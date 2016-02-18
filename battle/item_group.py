import pygame
import lib
from pygame.sprite import Sprite, Group
from util import get_file_path
from util.vector2 import Vector2
from random import randint

_rate = 150


class ItemGroup(Group):
    def __init__(self):
        Group.__init__(self)
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

    def render(self):
        for item in self.sprites():
            item.render()

    def drop_money(self, money, center):
        self.add(MoneySprite(money, center, self.money_images[0]))


class MoneySprite(Sprite):
    def __init__(self, money, center, money_images):
        Sprite.__init__(self)
        self.images = money_images
        self.money = money
        self.center = Vector2((center[0], center[1]-20))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_size()
        self.set_destination((0, 0))
        self.speed = 10
        self.passed_time = 0
        self.states = {}
        self.active_state = None
        self.add_state(AppearState(self))
        self.set_state('appear')

    def render(self):
        self.passed_time += lib.data.frame_time
        self.think()

    def move(self):
        img_index = int(self.passed_time / _rate) % 4
        self.image = self.images[img_index]
        self.center += self.vector_to_destination * self.speed
        x, y = self.center[0]-self.w/2, self.center[1]-self.h/2
        lib.draw.draw_image(self.image, (x, y))

    def set_destination(self, x_or_pair, y=None):
        if y is None:
            self.destination = Vector2(x_or_pair)
        else:
            self.destination = Vector2(x_or_pair, y)
        self.vector_to_destination = Vector2.from_points(
            self.center, self.destination).normalized()

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
        self.sprite.set_destination(0, 0)
