import pygame
import lib
from pygame.sprite import Group
from util import get_file_path


class MobGroup(Group):
    def __init__(self, mob_id, level):
        Group.__init__(self)
        if not isinstance(mob_id, list):
            raise TypeError('argument 2 must be list type')
        self.mob_info_list = {}
        self.mob_images = {}
        self.mob_type_count = 0
        for _id in mob_id:
            _datas = lib.pkl.load_mob_data(_id)
            # only keep the data's 'info' part
            _tmp_data = {
                'id': _datas['info']['id'],
                'hp': eval(_datas['info']['hp_curve'] % level),
                'money': eval(_datas['info']['money_curve'] % level),
                'speed': _datas['info']['speed'],
                'items': [_tuple for _tuple in _datas['items']]}
            self.mob_info_list[_id] = _tmp_data
            # get each action sub-surface from origin image
            _image_origin = self._load_image(_id)
            _tmp_dict = {}
            for _act_key in _datas['actions']:
                _tmp_list = []
                for _subsur_data in _datas['actions'][_act_key]:
                    _tmp_list.append(_image_origin.subsurface(
                        _subsur_data['topleft'], _subsur_data['size']))
                _tmp_dict[_act_key] = _tmp_list
            self.mob_images[_id] = _tmp_dict
            self.mob_type_count += 1

    def render(self):
        for mob in self.sprites():
            mob.update()
            mob.render()

    def collide(self, pos):
        _hit_mob_list = []
        for _mob in self.sprites():
            _hit_mob = _mob.collide(pos)
            if _hit_mob:
                _hit_mob_list.append(_hit_mob)
        return _hit_mob_list

    def get_mob_info(self, mob_id):
        return self.mob_info_list[mob_id]

    def get_mob_images(self, mob_id):
        return self.mob_images[mob_id]

    def add(self, *mob):
        Group.add(self, *mob)

    def mob_count(self):
        return len(self.sprites())

    def _load_image(self, mob_id):
        return pygame.image.load(
            get_file_path('img/mob/'+mob_id+'.png')).convert_alpha()
