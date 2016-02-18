import lib
from stages.base_stage import BaseStage
from battle.field import Field


class TestStage(BaseStage):
    def __init__(self):
        BaseStage.__init__(self)

    def init(self, initargs):
        mapdata = lib.pkl.load_map_data(initargs['mapname'])
        self.mob_id = mapdata['mob_id']
        self.field = Field(mapdata)

    def update(self):
        self.field.update()
