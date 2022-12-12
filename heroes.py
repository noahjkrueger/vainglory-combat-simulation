class Hero:
    def __init__(self, name, level, stutter):
        self.name = name
        self.items = list()
        self.stats = {
            "level": level, "stutter": stutter, "crit_damage": 0.5, "ismelee": False,
            "attack_cooldown": 0, "attack_delay": 0, "ss_penalty": 0, "as_modifier": 0, "base_hp": 0,
            "bonus_hp": 0, "current_hp": 0, "hp_regen": 0.0, "base_energy": 0, "energy": 0, "energy_regen": 0,
            "energy_regen_multi": 1.0, "wp": 0, "cp": 0, "move_speed_ratio": 1.0, "heal_barrier_multi": 1.0,
            "base_as": 0, "bonus_as": 0.0, "armor": 0, "shield": 0, "attack_range": 0, "move_speed": 0,
            "base_move_speed": 0, "vampirism": 0.0, "crit_chance": 0.0, "cooldown": 0.0, "armor_peirce": 0.0,
            "shield_peirce": 0.0, "crystal_lifesteal": 0, "uses_focus": False, "base_focus": 0,  "focus": 0,
            "focus_regen": 0
        }
        self.timers = {
            "attack": {
                "attack_delay": 0,
                "attack_cooldown": 0
            },
            "regen": {
                "delay": 1000
            }
        }
        self.debuffs = {
                "stun": {
                    "duration": 0
                },
                "silence": {
                    "duration": 0
                },
                "slow": {
                    "duration": 0,
                    "strength": 0
                },
                "mortal_wounds": {
                    "duration": 0
                },
                "atlas_pauldron": {
                    "duration": 0
                }
            }

    def _is_melee(self):
        self.stats['ismelee'] = True

    def _set_as_factors(self, cooldown, delay, ss_penalty, modifier):
        self.stats["attack_cooldown"] = cooldown
        self.stats["attack_delay"] = delay
        self.stats["ss_penalty"] = ss_penalty
        self.stats["as_modifier"] = modifier
        self.timers["attack"]["attack_delay"] = delay
        if self.stats["stutter"]:
            self.timers["attack"]["attack_delay"] += ss_penalty

    def _set_base_hp(self, at_level_1, at_level_12):
        self.stats["base_hp"] = self._calc_base_stat((at_level_1, at_level_12))

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
        self.stats["current_hp"] = self.stats["base_hp"] + self.stats["bonus_hp"]
        self.stats["move_speed"] += self.stats["base_move_speed"] * self.stats["move_speed_ratio"]

    def _get_attack_template(self):
        return {
            "true_dmg": 0.0,
            "wp_dmg": 0.0,
            "cp_dmg": 0.0,
            "armor_peirce": self.stats["armor_peirce"],
            "shield_peirce": self.stats["shield_peirce"],
            "hit": False,
            "on_minion": False,
            "kill_minion": False,
            "on_hero": False,
            "with_basic": False,
            "debuffs": {
                "stun": {
                    "duration": 0
                },
                "silence": {
                    "duration": 0
                },
                "slow": {
                    "duration": 0,
                    "strength": 0
                },
                "mortal_wounds": {
                    "duration": 0
                },
                "atlas_pauldron": {
                    "duration": 0
                }
            }
        }

    def attack(self):
        return self._basic_attack()

    def _basic_attack(self):
        # Get attack template, set as basic on hero
        the_attack = self._get_attack_template()
        the_attack["on_hero"] = True
        the_attack["with_basic"] = True
        # Hero hits at this ms
        if not self.timers["attack"]["attack_cooldown"]:
            # There is no hit but reduce delay
            if self.timers["attack"]["attack_delay"]:
                self.timers["attack"]["attack_delay"] -= 1
                return the_attack
            # There is a hit
            the_attack["hit"] = True
            self.timers["attack"]["attack_cooldown"] = round(self.stats["attack_cooldown"] / (self.stats["base_as"]
                + (self.stats["bonus_as"] * self.stats["as_modifier"])))
            # AP halfs total AS -> doubles attack_cooldown
            if self.debuffs["atlas_pauldron"]["duration"]:
                self.timers["attack"]["attack_cooldown"] *= 2
            if not self.stats["stutter"]:
                self.timers["attack"]["attack_delay"] += self.stats["ss_penalty"]
            self.timers["attack"]["attack_delay"] = self.stats["attack_delay"]
        # there is no hit but reduce cooldown
        elif self.timers["attack"]["attack_cooldown"] > 0:
            self.timers["attack"]["attack_cooldown"] -= 1
            return the_attack
        # Base Weapon Damage
        the_attack["wp_dmg"] = self.stats["wp"] if the_attack["hit"] else 0
        # Consider Item Buffs for basic attacks
        for item in self.items:
            try:
                the_attack = item.on_attack(self, the_attack)
            except AttributeError:
                continue
        # expected weapon dmg on crit
        if self.stats["crit_chance"]:
            the_attack["wp_dmg"] *= 1 + (self.stats["crit_damage"] * min(self.stats["crit_chance"], 1))
        # AP reduces wp_dmg by 30%
        if self.debuffs["atlas_pauldron"]["duration"]:
            the_attack["wp_dmg"] *= 0.7
        # report the calculations
        return the_attack

    def receive_attack(self, the_attack):
        ack = {
            "true_dmg": the_attack['true_dmg'],
            "on_hero": True,
            "prevent_cc": False
        }
        # calc wp and cp dmg received
        wp_without_p = (the_attack["wp_dmg"] / (1 + (self.stats["armor"] / 100))) * (1 - the_attack["armor_peirce"])
        cp_without_p = the_attack["cp_dmg"] / (1 + (self.stats["shield"] / 100)) * (1 - the_attack["shield_peirce"])
        wp_with_p = the_attack["wp_dmg"] * the_attack["armor_peirce"]
        cp_with_p = the_attack["cp_dmg"] * the_attack["shield_peirce"]
        ack["cp_dmg"] = cp_with_p + cp_without_p
        ack["wp_dmg"] = wp_with_p + wp_without_p
        # check to see if any items trigger before taking damage
        for item in self.items:
            try:
                ack = item.on_damage_receive(self, ack, the_attack, pre_dmg=True)
            except AttributeError:
                continue
        # take the damage
        self.stats["current_hp"] -= (ack["true_dmg"] + ack["wp_dmg"] + ack["cp_dmg"])
        # check to see if any items trigger after taking damage
        for item in self.items:
            try:
                ack = item.on_damage_receive(self, ack, the_attack, pre_dmg=False)
            except AttributeError:
                continue
        # update debuff timers
        for effect in self.debuffs.keys():
            if self.debuffs[effect]["duration"]:
                self.debuffs[effect]["duration"] -= 1
        # the hit might have debuffed this hero
        if not ack["prevent_cc"]:
            for dbuff in the_attack["debuffs"].keys():
                for att, val in the_attack["debuffs"][dbuff].items():
                    if val:
                        self.debuffs[dbuff][att] = val
        # report back what happened
        return ack

    def process_attack_ack(self, ack):
        # regen hp and mp every second
        if not self.timers["regen"]["delay"]:
            self._regen_energy()
            self._regen_hp()
        else:
            self.timers["regen"]["delay"] -= 1
        result = {
            "recover": 0
        }
        # update/trigger item(s) post-attack
        for item in self.items:
            try:
                result = item.post_attack(self, ack, result)
            except AttributeError:
                continue
        # if mortal wounds, reduce healing
        if self.debuffs["mortal_wounds"]["duration"] > 0:
            result["recover"] /= 3
        # potential heal
        self.stats["current_hp"] = min(self.stats["base_hp"] + self.stats["bonus_hp"],  self.stats["current_hp"] + result["recover"])

    def _regen_energy(self):
        regen = self.stats["energy_regen"] * self.stats["energy_regen_multi"]
        self.stats["energy"] = max(self.stats["base_energy"], self.stats["energy"] + regen)

    def _regen_hp(self):
        self.stats["current_hp"] = min(self.stats["base_hp"] + self.stats["bonus_hp"], self.stats["current_hp"] + (self.stats["hp_regen"] * (self.stats["base_hp"] + self.stats["bonus_hp"])))

    def _warn(self, code, msg):
        print(f"\033[93m_WARN {code}:\033[0m \033[1m'{self.name}'\033[0m {msg}")

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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")
        self._warn("h-g", "ATTACK SPEED FACTORS are estimated. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")
        self._warn("h-g", "ATTACK SPEED FACTORS are estimated. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")
        self._warn("h-g", "ATTACK SPEED FACTORS are estimated. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")
        self._warn("h-g", "ATTACK SPEED FACTORS are estimated. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")


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
        self._warn("h-a", "ABILITIES either not implemented or considered in combat. May skew results.")
        self._warn("h-p", "HERO PERK either not implemented or considered in combat. May skew results.")
        self._warn("h-g", "ATTACK SPEED FACTORS are estimated. May skew results.")
