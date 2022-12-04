from random import random


class Hero:
    def __init__(self, name, level, hp_range, hp_regen_range, energy_range, energy_regen_range, wp_range, cp_range, as_range, armor_range, shield_range, attack_range, move_speed):
        def calc_base_stat(stat_range, at_level):
            return (at_level - 1) * ((stat_range[1] - stat_range[0]) / 11) + stat_range[0]
        self.name = name
        self.items = list()
        self.stats = {
            "base_hp": calc_base_stat(hp_range, level),
            "current_hp": calc_base_stat(hp_range, level),
            "hp_regen": calc_base_stat(hp_regen_range, level),
            "energy": calc_base_stat(energy_range, level),
            "energy_regen": calc_base_stat(energy_regen_range, level),
            "wp": calc_base_stat(wp_range, level),
            "cp": calc_base_stat(cp_range, level),
            "as": calc_base_stat(as_range, level),
            "armor": calc_base_stat(armor_range, level),
            "shield": calc_base_stat(shield_range, level),
            "attack_range": attack_range,
            "move_speed": move_speed,
            "vampirism": 0.0,
            "crit_chance": 0.0,
            "crit_damage": 0.5,
            "cooldown": 0.0,
            "armor_peirce": 0.0,
            "shield_peirce": 0.0,
            "item_passives": dict(),
            "item_actives": dict(),
            "hero_passives": dict()
        }

    def init_build(self, build):
        for item in build:
            self.items.append(item.name)
            for k, v in item.changes.items():
                if k == "item_passives":
                    for p_name, p_func in v.items():
                        self.stats["item_passives"][p_name] = p_func
                elif k == "item_actives":
                    for p_name, p_func in v.items():
                        self.stats["item_passives"][p_name] = p_func
                elif k == "vampirism":
                    self.stats["vampirism"] = max(self.stats["vampirism"], v)
                elif k == "cooldown":
                    self.stats["cooldown"] = min(self.stats["cooldown"] + v, 0.35)
                elif k == "move_speed":
                    self.stats["move_speed"] = max(self.stats["move_speed"], v)
                else:
                    self.stats[k] += v
        self.stats["current_hp"] = self.stats["base_hp"]

    def send_attack(self, ms):
        the_attack = {
            "true_dmg": 0.0,
            "wp_dmg": 0.0,
            "cp_dmg": 0.0,
            "armor_peirce": 0.0,
            "shield_peirce": 0.0
        }
        if ms % round(1000 / self.stats["as"]) == 0:
            the_attack["wp_dmg"] = self.stats["wp"]
            if "Tension Bow" in self.stats["item_passives"]:
                the_attack["wp_dmg"] += self.stats["item_passives"]["Tension Bow"](the_attack["wp_dmg"])
            if "Breaking Point" in self.stats["item_passives"]:
                the_attack["wp_dmg"] += self.stats["item_passives"]["Breaking Point"](the_attack["wp_dmg"])
            if random() < self.stats["crit_chance"]:
                the_attack["wp_dmg"] *= 1 + self.stats["crit_damage"]
            the_attack["cp_dmg"] = self.stats["cp"]
        return the_attack

    def process_attack_ack(self, ms, ack):
        if "Breaking Point" in self.stats["item_passives"]:  # TODO: recalc bp stacks
            self.stats["item_passives"]["Breaking Point"](ack["wp_dmg"], update=True, ms=ms)

    def receive_attack(self, ms, the_attack):
        ack = {
            "cp_dmg": 0.0,
            "wp_dmg": the_attack["wp_dmg"],
            "true_dmg": 0.0
        }
        self.stats["current_hp"] -= the_attack["wp_dmg"]
        #TODO: rm hp
        return ack


class Miho(Hero):
    def __init__(self, level):
        super().__init__("Miho", level, (775, 2084), (0, 0), (0, 0), (0, 0), (75, 152), (0, 0), (1.0, 1.363), (25, 75), (20, 55), 3, 4)
        self._get_passives()

    def _get_passives(self):
        self.stats["hero_passives"] = list()  # TODO
