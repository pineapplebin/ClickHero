from util import check_chance


class Player:
    def __init__(self):
        # load save file
        self.level = 5
        self.critical_chance = 10
        self.damage = 10

    def do_damage(self):
        damage = self.damage
        is_critical = False
        if check_chance(self.critical_chance):
            damage += int(self.damage * 0.5)
            is_critical = True
        return damage, is_critical
