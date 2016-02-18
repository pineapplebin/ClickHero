from stages.menu_stage import MenuStage
from stages.test_stage import TestStage
from stages.loading_stage import LoadingStage
from stages.battle_stage import BattleStage


class StageFactory:
    def __init__(self):
        pass

    def create(self, stagename):
        return eval(stagename.capitalize()+'Stage')()
