class Hero:
    def __init__(self, name, level, hp_range, hp_regen_range, energy_range, energy_regen_range, wp_range, cp_range, as_range, armor_range, shield_range, attack_range, move_speed, ismelee, crtysal_lifesteal):
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
            "base_move_speed": move_speed,
            "vampirism": 0.0,
            "crit_chance": 0.0,
            "crit_damage": 0.5,
            "cooldown": 0.0,
            "armor_peirce": 0.0,
            "shield_peirce": 0.0,
            "item_passives": dict(),
            "item_actives": dict(),
            "hero_passives": dict(),
            "mortal_wounds_timer": 0,
            "ismelee": ismelee,
            "crystal_lifesteal": crtysal_lifesteal
        }

    def init_build(self, build):
        for item in build:
            self.items.append(item.name)
            for k, v in item.changes.items():
                if k == "item_passives":
                    for i, d in v.items():
                        self.stats["item_passives"][i] = d
                elif k == "item_actives":
                    for i, d in v.items():
                        self.stats["item_passives"][i] = d
                elif k == "vampirism":
                    self.stats["vampirism"] = max(self.stats["vampirism"], v)
                elif k == "cooldown":
                    self.stats["cooldown"] = min(self.stats["cooldown"] + v, 0.35)
                elif k == "move_speed":
                    self.stats["move_speed"] = max(self.stats["move_speed"], v)
                elif k == "crystal_lifesteal":
                    self.stats["crystal_lifesteal"] = max(self.stats["crystal_lifesteal"], v)
                else:
                    self.stats[k] += v
        self.stats["current_hp"] = self.stats["base_hp"]

    def basic_attack(self, ms):
        the_attack = {
            "true_dmg": 0.0,
            "wp_dmg": 0.0,
            "cp_dmg": 0.0,
            "armor_peirce": self.stats["armor_peirce"],
            "shield_peirce": self.stats["shield_peirce"],
            "mortal_wounds": 0
        }
        # Hero hits at this ms
        hit = ms % round(1000 / self.stats["as"]) == 0
        # Calc wp dmg
        the_attack["wp_dmg"] = self.stats["wp"] if hit else 0
        # update item passives based on hit
        if "Tornado Trigger" in self.stats["item_passives"].keys():
            self.stats["item_passives"]["Tornado Trigger"](self, hit)
        if "Bone Saw" in self.stats["item_passives"].keys():
            the_attack["armor_peirce"] += self.stats["item_passives"]["Bone Saw"](hit)
        if hit and "Poisoned Shiv" in self.stats["item_passives"].keys():
            the_attack["mortal_wounds"] = self.stats["item_passives"]["Poisoned Shiv"](self)
        if hit and "Minion's Foot" in self.stats["item_passives"].keys():
            self.stats["item_passives"]["Minion's Foot"](self)
        if hit and "Breaking Point" in self.stats["item_passives"].keys():
            the_attack['wp_dmg'] += self.stats["item_passives"]["Breaking Point"](self, hit)
        if hit and "Tension Bow" in self.stats["item_passives"].keys():
            the_attack['wp_dmg'] += self.stats["item_passives"]["Tension Bow"](self, hit)
        # expected wp dmg on crit
        if self.stats["crit_chance"]:
            the_attack["wp_dmg"] *= (1 + self.stats["crit_damage"]) * min(self.stats["crit_chance"], 1)
        return the_attack

    def receive_attack(self, ms, the_attack):
        ack = {
            "true_dmg": the_attack['true_dmg']
        }
        # calc wp and cp dmg recived
        wp_without_p = (the_attack["wp_dmg"] / (1 + (self.stats["armor"] / 100))) * (1 - the_attack["armor_peirce"])
        cp_without_p = the_attack["cp_dmg"] / (1 + (self.stats["shield"] / 100)) * (1 - the_attack["shield_peirce"])
        wp_with_p = the_attack["wp_dmg"] * the_attack["armor_peirce"]
        cp_with_p = the_attack["cp_dmg"] * the_attack["shield_peirce"]
        ack["cp_dmg"] = cp_with_p + cp_without_p
        ack["wp_dmg"] = wp_with_p + wp_without_p
        # take the damage
        self.stats["current_hp"] -= (ack["true_dmg"] + ack["wp_dmg"] + ack["cp_dmg"])
        # update mortal wounds timer
        if the_attack["mortal_wounds"] > 0:
            self.stats["mortal_wounds_timer"] = the_attack["mortal_wounds"]
        elif self.stats["mortal_wounds_timer"] > 0:
            self.stats["mortal_wounds_timer"] -= 1
        return ack

    def process_attack_ack(self, ack):
        recover = 0
        recover += self.stats["vampirism"] * ack["wp_dmg"] #TODO: max() w/ serp mask passive
        recover += self.stats["crystal_lifesteal"] * ack["cp_dmg"] #TODO: max() w/ eve passive
        if "Breaking Point" in self.stats["item_passives"].keys():
            self.stats["item_passives"]["Breaking Point"](self, True, damage_done=ack["wp_dmg"])
        self.stats["current_hp"] = min(self.stats["base_hp"],  self.stats["current_hp"] + recover)


class Miho(Hero):
    def __init__(self, level):
        super().__init__("Miho", level, (775, 2084), (0, 0), (0, 0), (0, 0), (75, 152), (0, 0), (1.0, 1.363), (25, 75), (20, 55), 3, 4, True, 0)
        self._get_passives()

    def _get_passives(self):
        self.stats["hero_passives"] = list()  # TODO
