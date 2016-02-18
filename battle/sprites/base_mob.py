import pygame
import lib
from lib.constant import *
from random import randint

_rate = 150
BAR_SIZE = (50, 9)


class BaseMob(pygame.sprite.Sprite):
    def __init__(self, fielddata, mobinfo, mobimgs):
        pygame.sprite.Sprite.__init__(self)
        self.mob_id = mobinfo['id']
        self.hp = mobinfo['hp']
        self.max_hp = mobinfo['hp']
        self.money = mobinfo['money']
        self.speed = mobinfo['speed']
        self.knockback = 3
        self.field_range = (fielddata[0]+1, fielddata[0]+fielddata[2]-1)
        self.images = mobimgs
        self.image = None
        self.rect = None
        self.bottomleft = [
            randint(*self.field_range), fielddata[1]+10]
        self.direction = [-1, 1][randint(0, 1)]
        self.passed_time = 0
        # state machine
        self.is_invicible = False
        self.states = {}
        self.active_state = None
        self.add_state(AppearState(self))
        self.add_state(MoveState(self))
        self.add_state(HitState(self))
        self.add_state(DieState(self))
        self.set_state('appear')

    def update(self):
        self.passed_time += lib.data.frame_time
        self.think()

    def render(self):
        _x, _y = self.bottomleft
        _w, _h = self.image.get_size()
        lib.draw.draw_image(self.image, (_x, _y-_h))
        _blanking = 5
        _bar_x = _x + _w / 2 - BAR_SIZE[0] / 2
        # _bar_y = _y - _h - _blanking - BAR_SIZE[1]
        _bar_y = _y + _blanking
        lib.draw.fill(C_BLACK, (_bar_x, _bar_y, BAR_SIZE[0], BAR_SIZE[1]))
        lib.draw.fill(
            C_WHITE, (_bar_x+1, _bar_y+1, BAR_SIZE[0]-2, BAR_SIZE[1]-2))
        lib.draw.fill(
            C_BLACK, (_bar_x+2, _bar_y+2, BAR_SIZE[0]-4, BAR_SIZE[1]-4))
        _bar_w = int(self.hp / self.max_hp * (BAR_SIZE[0]-6))
        lib.draw.fill(
            C_LIFEGREEN, (_bar_x+3, _bar_y+3, _bar_w, BAR_SIZE[1]-6))

    def collide(self, pos):
        if self.rect and not self.is_invicible:
            if self.rect.collidepoint(pos):
                return self
        return None

    def hit(self, damage):
        # 此后可以通过伤害触发其他行为
        self.hp -= damage
        self.set_state('hit')

    def is_die(self):
        if self.hp <= 0:
            return True

    def get_pos(self, point='bottomleft'):
        if not self.image:
            return None
        _w, _h = self.image.get_size()
        if point == 'bottomleft':
            return self.bottomleft[0], self.bottomleft[1]
        elif point == 'center':
            return self.bottomleft[0]+_w/2, self.bottomleft[1]-_h/2
        elif point == 'bottomcenter':
            return self.bottomleft[0]+_w/2, self.bottomleft[1]
        elif point == 'topcenter':
            return self.bottomleft[0]+_w/2, self.bottomleft[1]-_h

    def set_image(self, state_key, index):
        _is_filp = True if self.direction > 0 else False
        self.image = pygame.transform.flip(
            self.images[state_key][index],
            _is_filp, False)

    def _animate(self, is_move=False):
        _frame_index = int(self.passed_time / _rate) %\
            len(self.images[self.active_state.name])
        _is_filp = True if self.direction > 0 else False
        self.image = pygame.transform.flip(
            self.images[self.active_state.name][_frame_index],
            _is_filp, False)
        if is_move:
            self.bottomleft[0] += self.direction *\
                lib.data.frame_time / 1000 * self.speed
        self.rect = self.image.get_rect(
            bottomleft=self.bottomleft)

    # state machine
    def add_state(self, state):
        self.states[state.name] = state

    def think(self):
        if not self.active_state:
            return
        self.active_state.do_action()
        if self.active_state.is_die() and self.active_state.name != 'die':
            self.active_state.next_state = 'die'
        else:
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
        pass

    def check_condition(self):
        pass

    def exit_action(self):
        pass

    def is_die(self):
        if self.sprite.is_die():
            return True
        return False


class AppearState(State):
    def __init__(self, sprite):
        State.__init__(self, 'appear')
        self.sprite = sprite

    def do_action(self):
        self.sprite._animate()

    def check_condition(self):
        _frame_count = len(self.sprite.images[self.name])
        _time = _rate * (_frame_count - 0.5)
        if self.sprite.passed_time >= _time:
            self.next_state = 'move'


class HitState(State):
    def __init__(self, sprite):
        State.__init__(self, 'hit')
        self.sprite = sprite

    def do_action(self):
        self.sprite.set_image('die', 0)
        _test_pos = self.sprite.bottomleft[0] - (
            self.sprite.direction * self.sprite.passed_time /
            1000 * self.sprite.knockback)
        _w = self.sprite.image.get_size()[0]
        if _test_pos > self.sprite.field_range[0] and\
                _test_pos < self.sprite.field_range[1]-_w:
            self.sprite.bottomleft[0] = _test_pos

    def check_condition(self):
        if self.sprite.passed_time > _rate * 2:
            self.next_state = 'move'


class MoveState(State):
    def __init__(self, sprite):
        State.__init__(self, 'move')
        self.sprite = sprite

    def do_action(self):
        self.sprite._animate(True)
        _x = self.sprite.bottomleft[0]
        _w = self.sprite.image.get_size()[0]
        if _x <= self.sprite.field_range[0]:
            self.sprite.bottomleft[0] = self.sprite.field_range[0]
            self.sprite.direction *= -1
        elif _x >= self.sprite.field_range[1]-_w:
            self.sprite.bottomleft[0] = self.sprite.field_range[1]-_w
            self.sprite.direction *= -1


class DieState(State):
    def __init__(self, sprite):
        State.__init__(self, 'die')
        self.sprite = sprite

    def entry_action(self):
        State.entry_action(self)
        self.sprite.is_invicible = True

    def do_action(self):
        self.sprite._animate()

    def check_condition(self):
        _frame_count = len(self.sprite.images[self.name])
        _time = _rate * (_frame_count - 0.5)
        if self.sprite.passed_time >= _time:
            self.sprite.kill()
