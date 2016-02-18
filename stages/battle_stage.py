import lib
import battle
from stages.base_stage import BaseStage
from battle.field import Field
from battle.mob_group import MobGroup
from battle.item_group import ItemGroup
from battle.sprites.base_mob import BaseMob
from util import check_chance, randindex


class BattleStage(BaseStage):
    """
    战斗场景类
    内部包括有场地渲染的Field实例,精灵组MobGroup实例
    """
    def __init__(self):
        BaseStage.__init__(self)
        self.field_level = lib.player.level
        self.item_group = None

    def init(self, initargs):
        battle.effect.init()
        mapdata = lib.pkl.load_map_data(initargs['mapname'])
        self.mob_id = mapdata['mob_id']
        self.field = Field(mapdata)
        self.mob_group = MobGroup(self.mob_id, self.field_level)
        if not self.item_group:
            self.item_group = ItemGroup()
        self.create_mob()

    def update(self):
        self.field.render()
        if self.mob_group.mob_count() < 10 and check_chance(1):
            self.create_mob()
        if lib.event.mouse_unpressed == 1:
            _hit_mob_list = self.mob_group.collide(lib.event.mouse_pos)
            if len(_hit_mob_list) > 0:
                self.battle_clear(_hit_mob_list)
        elif lib.event.mouse_pressed == 3:
            self.item_group.collide(lib.event.mouse_pos)
        self.mob_group.render()
        self.item_group.render()
        battle.effect.render()

    def exit(self):
        self.field.empty()
        self.mob_group.empty()

    def battle_clear(self, mob_list):
        damage, is_critical = lib.player.do_damage()
        for _mob in mob_list:
            _mob.hit(damage)
            _x, _y = _mob.get_pos('topcenter')
            battle.effect.new_damage(damage, (_x, _y-10), is_critical)
            if _mob.is_die():
                _money = _mob.money
                _item_id = _mob.drop_item()
                _pos = (_mob.get_pos('bottomcenter'))
                self.item_group.drop_money(_money, _pos)
                if _item_id:
                    self.item_group.drop_item(_item_id, _pos)

    def create_mob(self):
        _mob_id = self.mob_id[randindex(len(self.mob_id))]
        self.mob_group.add(BaseMob(
            self.field.get_rand_field(),
            self.mob_group.get_mob_info(_mob_id),
            self.mob_group.get_mob_images(_mob_id)))
