from util import check_chance


class Player:
    def __init__(self):
        # load save file
        self.level = 10
        self.critical_chance = 10
        self.damage = 10
        self.hit_num = 5
        self.critical_power = 50

    def do_damage(self):
        total_damage = 0
        damage_list = []
        for _ in range(self.hit_num):
            damage = self.damage
            is_critical = False
            if check_chance(self.critical_chance):
                damage += int(self.damage * self.critical_power / 100)
                is_critical = True
            total_damage += damage
            damage_list.append((damage, is_critical))
        return total_damage, sorted(damage_list, key=lambda dmg: dmg[1])
