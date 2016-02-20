import lib
from view.base_stage import BaseStageView
from model.field import FieldModel


class TestStageView(BaseStageView):
    def __init__(self):
        BaseStageView.__init__(self)

    def init(self, initargs):
        mapdata = lib.pkl.load_map_data(initargs['mapname'])
        self.mob_id = mapdata['mob_id']
        self.field = FieldModel(mapdata)

    def render(self):
        self.field.update()
