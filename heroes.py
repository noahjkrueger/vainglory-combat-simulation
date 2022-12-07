class Hero:
    def __init__(self, name, level, stutter):
        self.name = name
        self.items = list()
        self.stats = {
            "level": level, "stutter": stutter, "crit_damage": 0.5, "ismelee": False,
            "attack_cooldown": 0, "attack_delay": 0, "ss_penalty": 0, "as_modifier": 0, "base_hp": 0,
            "current_hp": 0, "hp_regen": 0, "base_energy": 0, "energy": 0, "energy_regen": 0, "wp": 0, "cp": 0,
            "base_as": 0, "bonus_as": 0.0, "armor": 0, "shield": 0, "attack_range": 0, "move_speed": 0,
            "base_move_speed": 0, "vampirism": 0.0, "crit_chance": 0.0, "cooldown": 0.0, "armor_peirce": 0.0,
            "shield_peirce": 0.0, "hero_passives": dict(), "mortal_wounds_timer": 0, "crystal_lifesteal": 0,
            "uses_focus": False, "base_focus": 0,  "focus": 0, "focus_regen": 0,
        }

    def _is_melee(self):
        self.stats['ismelee'] = True

    def _set_as_factors(self, cooldown, delay, ss_penalty, modifier):
        self.stats["attack_cooldown"] = cooldown
        self.stats["attack_delay"] = delay
        self.stats["ss_penalty"] = ss_penalty
        self.stats["as_mpdifier"] = modifier

    def _set_base_hp(self, at_level_1, at_level_12):
        self.stats["base_hp"] = self._calc_base_stat((at_level_1, at_level_12))
        self.stats["current_hp"] = self.stats["base_hp"]

    def _set_hp_regen(self, at_level_1, at_level_12):
        self.stats["hp_regen"] = self._calc_base_stat((at_level_1, at_level_12))

    def _set_base_energy(self, at_level_1, at_level_12):
        self.stats["base_energy"] = self._calc_base_stat((at_level_1, at_level_12))
        self.stats["energy"] = self.stats["base_energy"]

    def _set_energy_regen(self, at_level_1, at_level_12):
        self.stats["energy_regen"] = self._calc_base_stat((at_level_1, at_level_12))

    def _set_wp(self, at_level_1, at_level_12):
        self.stats["wp"] = self._calc_base_stat((at_level_1, at_level_12))

    def _set_cp(self, at_level_1, at_level_12):
        self.stats["cp"] = self._calc_base_stat((at_level_1, at_level_12))

    def _set_base_as(self, at_level_1, at_level_12):
        self.stats["base_as"] = self._calc_base_stat((at_level_1, at_level_12))

    def _set_armor(self, at_level_1, at_level_12):
        self.stats["armor"] = self._calc_base_stat((at_level_1, at_level_12))

    def _set_shield(self, at_level_1, at_level_12):
        self.stats["shield"] = self._calc_base_stat((at_level_1, at_level_12))

    def _set_attack_range(self, val):
        self.stats["attack_range"] = val

    def _set_base_move_speed(self, val):
        self.stats["base_move_speed"] = val

    def _calc_base_stat(self, stat_range):
        return (self.stats['level'] - 1) * ((stat_range[1] - stat_range[0]) / 11) + stat_range[0]

    def _uses_focus(self, limit, regen):
        self.stats["used_focus"] = True
        self.stats["base_focus"] = limit
        self.stats["focus"] = self.stats["base_focus"]
        self.stats["focus_regen"] = regen

    def init_build(self, build):
        for item in build:
            self.items.append(item)
            for k, v in item.changes.items():
                # These do not stack or have limits
                if k == "vampirism":
                    self.stats["vampirism"] = max(self.stats["vampirism"], v)
                elif k == "cooldown":
                    self.stats["cooldown"] = min(self.stats["cooldown"] + v, 0.35)
                elif k == "move_speed":
                    self.stats["move_speed"] = max(self.stats["move_speed"], v)
                elif k == "crystal_lifesteal":
                    self.stats["crystal_lifesteal"] = max(self.stats["crystal_lifesteal"], v)
                # Regular Stat change
                else:
                    self.stats[k] += v
        # Set current HP
        self.stats["current_hp"] = self.stats["base_hp"]

    def basic_attack(self, ms):
        the_attack = {
            "true_dmg": 0.0,
            "wp_dmg": 0.0,
            "cp_dmg": 0.0,
            "armor_peirce": self.stats["armor_peirce"],
            "shield_peirce": self.stats["shield_peirce"],
            "mortal_wounds": 0,
            "hit": False,
            "on_minion": False,
            "on_hero": True,
            "with_basic": True
        }
        # Hero hits at this ms
        att_time = self.stats["attack_delay"] + (self.stats["attack_cooldown"] / (self.stats["base_as"]
            + (self.stats["bonus_as"] * self.stats["as_modifier"]))) \
            + (self.stats["ss_penalty"] if not self.stats["stutter"] else 0)
        if ms % round(att_time) == 0:
            the_attack["hit"] = True
        # Base Weapon Damage
        the_attack["wp_dmg"] = self.stats["wp"] if the_attack["hit"] else 0
        # Consider Item Buffs
        for item in self.items:
            try:
                the_attack = item.on_hit(self, the_attack)
            except AttributeError:
                continue
        # expected weapon dmg on crit
        if self.stats["crit_chance"]:
            the_attack["wp_dmg"] *= (1 + self.stats["crit_damage"]) * min(self.stats["crit_chance"], 1)
        return the_attack

    def receive_attack(self, the_attack):
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
        for item in self.items:
            try:
                ack = item.on_damage_recive(self, the_attack)
            except AttributeError:
                continue
        # take the damage
        self.stats["current_hp"] -= (ack["true_dmg"] + ack["wp_dmg"] + ack["cp_dmg"])
        # update mortal wounds timer
        if the_attack["mortal_wounds"] > 0:
            self.stats["mortal_wounds_timer"] = the_attack["mortal_wounds"]
        elif self.stats["mortal_wounds_timer"] > 0:
            self.stats["mortal_wounds_timer"] -= 1
        return ack

    def process_attack_ack(self, ack):
        result = {
            "recover": 0
        }
        for item in self.items:
            try:
                result = item.post_hit(self, ack, result)
            except AttributeError:
                continue
        if self.stats["mortal_wounds_timer"]:
            result["recover"] /= 3
        self.stats["current_hp"] = min(self.stats["base_hp"],  self.stats["current_hp"] + result["recover"])


class Amael(Hero):
    def __init__(self, level, stutter):
        super().__init__("Amael", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0) # Guess
        super()._set_base_hp(830, 2502)
        super()._set_base_energy(275, 550)
        super()._set_energy_regen(1.87, 4.29)
        super()._set_attack_range(1.6)
        super()._set_base_move_speed(3.9)
        super()._set_base_as(1.0, 1.22)
        super()._set_armor(30, 85)
        super()._set_shield(20, 60)
        super()._set_wp(86, 152)
        # TODO: hero perk and abilities


class Adagio(Hero):
    def __init__(self, level, stutter):
        super().__init__("Adagio", level, stutter)
        super()._set_as_factors(800, 250, 200, 1.0)
        super()._set_base_hp(685, 2308)
        super()._set_base_energy(400, 785)
        super()._set_energy_regen(2.67, 5.2)
        super()._set_attack_range(6)
        super()._set_base_move_speed(3.8)
        super()._set_base_as(1.0, 1.22)
        super()._set_armor(25, 75)
        super()._set_shield(20, 55)
        super()._set_wp(75, 117)
        # TODO: hero perk and abilities


class Alpha(Hero):
    def __init__(self, level, stutter):
        super().__init__("Alpha", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 250, 200, 1.0)
        super()._set_base_hp(761,  2537)
        super()._set_attack_range(2.1)
        super()._set_base_move_speed(4)
        super()._set_base_as(1.0, 1.363)
        super()._set_armor(30, 85)
        super()._set_shield(20, 60)
        super()._set_wp(83, 124)
        # TODO: hero perk and abilities


class Anka(Hero):
    def __init__(self, level, stutter):
        super().__init__("Anka", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0) # Guess
        super()._set_base_hp(750,  2301)
        super()._set_base_energy(200, 695)
        super()._set_energy_regen(2.6, 4.8)
        super()._set_attack_range(1.6)
        super()._set_base_move_speed(4)
        super()._set_base_as(1.0, 1.363)
        super()._set_armor(30, 85)
        super()._set_shield(20, 60)
        super()._set_wp(82, 152)
        # TODO: hero perk and abilities


class Ardan(Hero):
    def __init__(self, level, stutter):
        super().__init__("Ardan", level, stutter)
        super()._is_melee()
        super()._uses_focus(100, 10)
        super()._set_as_factors(800, 230, 200, 1.0)
        super()._set_base_hp(838, 2628)
        super()._set_attack_range(1.8)
        super()._set_base_move_speed(3.9)
        super()._set_base_as(1.0, 1.363)
        super()._set_armor(35, 100)
        super()._set_shield(25, 75)
        super()._set_wp(80, 140)
        # TODO: hero perk and abilities


class Baptiste(Hero):
    def __init__(self, level, stutter):
        super().__init__("Baptiste", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 250, 200, 1.0) # Guess
        super()._set_base_hp(739, 2323)
        super()._set_base_energy(273, 636)
        super()._set_energy_regen(2.17, 4.26)
        super()._set_attack_range(2.8)
        super()._set_base_move_speed(3.9)
        super()._set_base_as(1.0, 1.363)
        super()._set_armor(35, 85)
        super()._set_shield(20, 60)
        super()._set_wp(78, 167)
        # TODO: hero perk and abilities


class Baron(Hero):
    def __init__(self, level, stutter):
        super().__init__("Baron", level, stutter)
        super()._set_as_factors(1000, 500, 200, 0.6)
        super()._set_base_hp(679, 2054)
        super()._set_base_energy(320, 815)
        super()._set_energy_regen(6.67, 18)
        super()._set_attack_range(5.8)
        super()._set_base_move_speed(3.6)
        super()._set_base_as(1.0, 1.11)
        super()._set_armor(26, 78)
        super()._set_shield(21, 57)
        super()._set_wp(71, 130)
        # TODO: hero perk and abilities


class Blackfeather(Hero):
    def __init__(self, level, stutter):
        super().__init__("Blackfeather", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0)
        super()._set_base_hp(657, 2387)
        super()._set_attack_range(1.8)
        super()._set_base_move_speed(3.9)
        super()._set_base_as(1.0, 1.22)
        super()._uses_focus(100, 10)
        super()._set_armor(25, 75)
        super()._set_shield(20, 55)
        super()._set_wp(81, 160)
        # TODO: hero perk and abilities


class Caine(Hero):
    def __init__(self, level, stutter):
        super().__init__("Caine", level, stutter)
        super()._set_as_factors(800, 350, 200, 1.0) # guess
        super()._set_base_hp(750, 2048)
        super()._set_attack_range(6.4)
        super()._set_base_move_speed(3.8)
        super()._set_base_as(1.0, 1.22)
        super()._set_armor(25, 74)
        super()._set_shield(20, 58)
        super()._set_wp(82, 159)
        # TODO: hero perk and abilities


class Catherine(Hero):
    def __init__(self, level, stutter):
        super().__init__("Catherine", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0)
        super()._set_base_hp(808,  2673)
        super()._set_base_energy(200, 464)
        super()._set_energy_regen(1.33, 3.09)
        super()._set_attack_range(1.5)
        super()._set_base_move_speed(4.1)
        super()._set_base_as(1.0, 1.363)
        super()._set_armor(35, 100)
        super()._set_shield(25, 75)
        super()._set_wp(74, 141)
        # TODO: hero perk and abilities


class Celeste(Hero):
    def __init__(self, level, stutter):
        super().__init__("Celeste", level, stutter)
        super()._set_as_factors(800, 300, 200, 1.0)
        super()._set_base_hp(649, 2028)
        super()._set_base_energy(380, 732)
        super()._set_energy_regen(2.53, 4.84)
        super()._set_attack_range(5.3)
        super()._set_base_move_speed(3.8)
        super()._set_base_as(1.0, 1.25)
        super()._set_armor(25, 75)
        super()._set_shield(20, 55)
        # TODO: hero perk and abilities


class Churnwalker(Hero):
    def __init__(self, level, stutter):
        super().__init__("Churnwalker", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0) # guess
        super()._set_base_hp(863,  2749)
        super()._set_base_energy(380, 732)
        super()._set_energy_regen(2.38, 4.69)
        super()._set_attack_range(1.7)
        super()._set_base_move_speed(3.7)
        super()._set_base_as(1.0, 1.22)
        super()._set_armor(35, 100)
        super()._set_shield(25, 75)
        super()._set_wp(80, 165)
        # TODO: hero perk and abilities


class Flicker(Hero):
    def __init__(self, level, stutter):
        super().__init__("Flicker", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0)
        super()._set_base_hp(797,  2648)
        super()._set_base_energy(295, 757)
        super()._set_energy_regen(1.94, 4.69)
        super()._set_attack_range(1.5)
        super()._set_base_move_speed(3.9)
        super()._set_base_as(1.0, 1.363)
        super()._set_armor(35, 100)
        super()._set_shield(25, 75)
        super()._set_wp(77, 155)
        # TODO: hero perk and abilities


class Fortress(Hero):
    def __init__(self, level, stutter):
        super().__init__("Fortress", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0)
        super()._set_base_hp(761,  2581)
        super()._set_base_energy(300, 465)
        super()._set_energy_regen(1.56, 3.21)
        super()._set_attack_range(1.8)
        super()._set_base_move_speed(3.9)
        super()._set_base_as(1.0, 1.44)
        super()._set_armor(30, 85)
        super()._set_shield(20, 60)
        super()._set_wp(73, 156)
        # TODO: hero perk and abilities


class Glaive(Hero):
    def __init__(self, level, stutter):
        super().__init__("Glaive", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 230, 200, 1.0)
        super()._set_base_hp(834, 2503)
        super()._set_base_energy(275, 440)
        super()._set_energy_regen(1.47, 2.9)
        super()._set_attack_range(2.8)
        super()._set_base_move_speed(3.9)
        super()._set_base_as(1.0, 1.22)
        super()._set_armor(30, 85)
        super()._set_shield(20, 60)
        super()._set_wp(70, 156)
        # TODO: hero perk and abilities


class Grace(Hero):
    def __init__(self, level, stutter):
        super().__init__("Grace", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0)
        super()._set_base_hp(740,  2483)
        super()._set_base_energy(268, 653)
        super()._set_energy_regen(1.92, 4.23)
        super()._set_attack_range(2.7)
        super()._set_base_move_speed(4.1)
        super()._set_base_as(1.0, 1.363)
        super()._set_armor(30, 100)
        super()._set_shield(25, 75)
        super()._set_wp(73, 152)
        # TODO: hero perk and abilities


class Miho(Hero):
    def __init__(self, level, stutter):
        super().__init__("Miho", level, stutter)
        super()._is_melee()
        super()._set_as_factors(800, 300, 200, 1.0) # guess
        super()._set_base_hp(775, 2084)
        super()._set_attack_range(3)
        super()._set_base_move_speed(4)
        super()._set_base_as(1.0, 1.363)
        super()._uses_focus(100, 10)
        super()._set_armor(25, 75)
        super()._set_shield(20, 55)
        super()._set_wp(75, 152)
        # TODO: hero perk and abilities
