from view.menu_stage import MenuStageView
from view.test_stage import TestStageView
from view.loading_stage import LoadingStageView
from view.battle_stage import BattleStageView


class StageFactory:
    def __init__(self):
        self._stage_list = {
            'menu': MenuStageView,
            'loading': LoadingStageView,
            'battle': BattleStageView,
            'test': TestStageView
        }

    def create(self, stagename):
        return self._stage_list[stagename]()
