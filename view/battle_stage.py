import lib
import battle
from lib.constant import *
from view.base_controller import BaseController
from view.base_stage import BaseStageView
from model.field import FieldModel
from model.mob_group import MobGroupModel
from model.item_group import ItemGroupModel
from battle.sprites.base_mob import BaseMob
from util import check_chance, randindex

BAR_SIZE = (50, 9)


class BattleStageView(BaseStageView):
    """
    战斗场景类
    内部包括有场地渲染的Field实例,精灵组MobGroup实例
    """
    def __init__(self):
        BaseStageView.__init__(self)
        self.controller = BattleStageController(self)

    def init(self, initargs):
        self.controller.init(initargs)

    def render(self):
        self.controller.update()
        #: 检测输入
        if lib.event.mouse_unpressed == 1:
            self.controller.handle_player_attack()
        elif lib.event.mouse_pressed == 3:
            self.controller.handle_pick_item()
        #: 渲染场地
        for data in self.controller.field_model.get_render_data():
            lib.draw.draw_image(data[0], data[1])
        #: 渲染怪物和血条
        for data in self.controller.mob_group_model.get_render_data():
            lib.draw.draw_image(data[0], data[1])
            bar_x, bar_y = data[3][0] - BAR_SIZE[0] / 2, data[3][1] + 5
            lib.draw.fill(C_BLACK, (bar_x, bar_y, BAR_SIZE[0], BAR_SIZE[1]))
            lib.draw.fill(
                C_WHITE, (bar_x+1, bar_y+1, BAR_SIZE[0]-2, BAR_SIZE[1]-2))
            lib.draw.fill(
                C_BLACK, (bar_x+2, bar_y+2, BAR_SIZE[0]-4, BAR_SIZE[1]-4))
            _bar_w = int(data[2] * (BAR_SIZE[0]-6))
            lib.draw.fill(
                C_LIFEGREEN, (bar_x+3, bar_y+3, _bar_w, BAR_SIZE[1]-6))
        #: 渲染物品
        for data in self.controller.item_group_model.get_render_data():
            lib.draw.draw_image(data[0], data[1])
        #: 渲染效果
        battle.effect.render()

    def exit(self):
        self.field.empty()
        self.mob_group.empty()
        battle.effect.init()


class BattleStageController(BaseController):
    def init(self, initargs):
        mapdata = lib.pkl.load_map_data(initargs['mapname'])
        self.mob_id_list = mapdata['mob_id']
        self.mob_group_model = MobGroupModel(
            self.mob_id_list, lib.player.level)
        self.field_model = FieldModel(mapdata)
        if not hasattr(self, 'item_group_model'):
            self.item_group_model = ItemGroupModel()

    def update(self):
        if self.mob_group_model.mob_count() < 10:
            if check_chance(1):
                self.create_mob()

    def create_mob(self):
        _mob_id = self.mob_id_list[randindex(len(self.mob_id_list))]
        self.mob_group_model.add(BaseMob(
            self.field_model.get_rand_field(),
            self.mob_group_model.get_mob_info(_mob_id),
            self.mob_group_model.get_mob_images(_mob_id)))

    def handle_player_attack(self):
        _hit_mob_list = self.mob_group_model.collide(lib.event.mouse_pos)
        if len(_hit_mob_list) > 0:
            self.battle_clear(_hit_mob_list)

    def battle_clear(self, mob_list):
        total_damage, damage_list = lib.player.do_damage()
        for _mob in mob_list:
            _mob.hit(total_damage)
            _x, _y = _mob.get_pos('topcenter')
            battle.effect.new_damage(damage_list, (_x, _y-10))
            if _mob.is_die():
                _money = _mob.money
                _item_id = _mob.drop_item()
                _pos = (_mob.get_pos('bottomcenter'))
                self.item_group_model.drop_money(_money, _pos)
                if _item_id:
                    self.item_group_model.drop_item(_item_id, _pos)

    def handle_pick_item(self):
        self.item_group_model.collide(lib.event.mouse_pos)
