class Item:
    def __init__(self, name):
        self.name = name
        self.changes = dict()

    def _set_bonus_hp(self, val):
        self.changes["bonus_hp"] = val

    def _set_hp_regen(self, val):
        self.changes["hp_regen"] = val

    def _set_base_energy(self, val):
        self.changes["base_energy"] = val

    def _set_energy_regen(self, val):
        self.changes["energy_regen"] = val

    def _set_energy_regen_multi(self, val):
        self.changes["energy_regen_multi"] = val

    def _set_wp(self, val):
        self.changes["wp"] = val

    def _set_cp(self, val):
        self.changes["cp"] = val

    def _set_bonus_as(self, val):
        self.changes["bonus_as"] = val

    def _set_move_speed_ratio(self, val):
        self.changes["move_speed_ratio"] = val

    def _set_move_speed(self, val):
        self.changes["move_speed"] = val

    def _set_crit_chance(self, val):
        self.changes["crit_chance"] = val

    def _set_crit_damage(self, val):
        self.changes["crit_damage"] = val

    def _set_vampirism(self, val):
        self.changes["vampirism"] = val

    def _set_cooldown(self, val):
        self.changes["cooldown"] = val

    def _set_armor_peirce(self, val):
        self.changes["armor_peirce"] = val

    def _set_shield_peirce(self, val):
        self.changes["shield_peirce"] = val

    def _set_crystal_lifesteal(self, val):
        self.changes["crystal_lifesteal"] = val

    def _set_armor(self, val):
        self.changes["armor"] = val

    def _set_shield(self, val):
        self.changes["shield"] = val

    def warn(self, code, msg):
        print(f"\033[93mWARN {code}:\033[0m \033[1m'{self.name}'\033[0m - {msg}")


# Start of Red Tree
class BarbedNeedle(Item):
    def __init__(self):
        super().__init__("Barbed Needle")
        super()._set_wp(10)
        super()._set_vampirism(0.1)

    @staticmethod
    def on_attack(hero, the_attack):
        if the_attack["hit"] and the_attack["kill_minion"]:
            new_hp = hero.stats["current_hp"] + 30 if the_attack["with_basic"] else hero.stats["current_hp"] + 10
            hero.stats["current_hp"] = max(new_hp, hero.stats["base_hp"])
        return the_attack

    @staticmethod
    def post_attack(hero, ack, result):
        if not result["recover"]:
            result["recover"] = ack["wp_dmg"] * hero.stats["vampirism"]
        return result


class BoneSaw(Item):
    def __init__(self):
        super().__init__("Bone Saw")
        super()._set_wp(30)
        super()._set_armor_peirce(0.2)
        super()._set_bonus_as(0.3)

        self.__stacks = 0
        self.__timer = 0
        self.warn("i-i", "once decay is active (after 3s delay), stacks drop ever .1s. Negligible but may skew results.")

    def on_attack(self, hero, the_attack):
        if the_attack["hit"] and the_attack["with_basic"]:
            self.__stacks = min(self.__stacks + 1, 5)
            self.__timer = 3000
        the_attack["armor_peirce"] = max(self.__stacks * 0.1 + the_attack["armor_peirce"], the_attack["armor_peirce"])
        return the_attack

    def post_attack(self, hero, ack, result):
        if self.__timer > 0:
            self.__timer -= 1
        if self.__timer == 0 and self.__stacks > 0:
            self.__stacks -= 1
            self.__timer = 100
        return result


class BookOfEulogies(Item):
    def __init__(self):
        super().__init__("Book of Eulogies")
        super()._set_wp(5)
        super()._set_vampirism(0.05)

    @staticmethod
    def on_attack(hero, the_attack):
        if the_attack["hit"] and the_attack["kill_minion"]:
            new_hp = hero.stats["current_hp"] + 30 if the_attack["with_basic"] else hero.stats["current_hp"] + 10
            hero.stats["current_hp"] = max(new_hp, hero.stats["base_hp"])
        return the_attack

    @staticmethod
    def post_attack(hero, ack, result):
        if not result["recover"]:
            result["recover"] = ack["wp_dmg"] * hero.stats["vampirism"]
        return result


class BreakingPoint(Item):
    def __init__(self):
        super().__init__("Breaking Point")
        super()._set_wp(50)
        super()._set_bonus_as(0.2)

        self.__stacks = 0
        self.__timer = 0
        self.__leftover = 0

    def on_attack(self, hero, the_attack):
        if the_attack["hit"] and the_attack["with_basic"]:
            self.__timer = 2500
            the_attack["wp_dmg"] += 5 * self.__stacks
        return the_attack

    def post_attack(self, hero, ack, result):
        decay_stacks = True
        if ack["wp_dmg"] and ack["on_hero"]:
            acc_dmg = ack["wp_dmg"] + self.__leftover
            while True:
                dmg_needed = 100 + self.__stacks * (5 if hero.stats["ismelee"] else 10)
                if acc_dmg >= dmg_needed:
                    decay_stacks = False
                    if self.__stacks < 35:
                        self.__stacks += 1
                    acc_dmg -= dmg_needed
                else:
                    self.__leftover = acc_dmg
                    break

        if decay_stacks:
            if self.__timer > 0:
                self.__timer -= 1
            else:
                self.__stacks -= 1
                self.__timer = 200
        return result



class BlazingSalvo(Item):
    def __init__(self):
        super().__init__("Blazing Salvo")
        super()._set_bonus_as(0.2)


class HeavySteel(Item):
    def __init__(self):
        super().__init__("Heavy Steel")
        super()._set_wp(45)


class LuckyStrike(Item):
    def __init__(self):
        super().__init__("Lucky Strike")
        super()._set_crit_chance(0.2)
        super()._set_crit_damage(0.05)


class MinionsFoot(Item):
    def __init__(self):
        super().__init__("Minion's Foot")
        super()._set_crit_chance(0.1)
        super()._set_crit_damage(0.05)

        self.__is_first = True
        self._normal_crit_perc = 0.0

    def on_attack(self, hero, the_attack):
        if the_attack["hit"]:
            if self.__is_first:
                self._normal_crit_perc = hero.stats["crit_chance"]
                hero.stats["crit_chance"] = 1.0
                self.__is_first = False
            else:
                hero.stats["crit_chance"] = self._normal_crit_perc
        return the_attack


class PiercingSpear(Item):
    def __init__(self):
        super().__init__("Piercing Spear")
        super()._set_wp(15)
        super()._set_armor_peirce(0.1)


class PoisonedShiv(Item):
    def __init__(self):
        super().__init__("Poisoned Shiv")
        super()._set_wp(35)
        super()._set_bonus_as(0.35)
        super()._set_vampirism(0.1)

        self.__hit_num = 0
        self.warn("i-i", "- ignorable for 1v1, but this item only applies mortal wounds every 2 hits on same target. Current implementation does not consider change of target.")

    def on_attack(self, hero, the_attack):
        if the_attack["hit"] and the_attack["kill_minion"]:
            new_hp = hero.stats["current_hp"] + 25 if the_attack["with_basic"] else hero.stats["current_hp"] + 10
            hero.stats["current_hp"] = max(new_hp, hero.stats["base_hp"])
        if the_attack["hit"] and the_attack["with_basic"]:
            self.__hit_num = 1 if self.__hit_num == 2 else 2
            the_attack["mortal_wounds"] = max(the_attack["mortal_wounds"], 2000 if self.__hit_num == 2 else 0)
        return the_attack

    @staticmethod
    def post_attack(hero, ack, result):
        if not result["recover"]:
            result["recover"] = ack["wp_dmg"] * hero.stats["vampirism"]
        return result


class SerpentMask(Item):
    def __init__(self):
        super().__init__("Serpent Mask")
        super()._set_wp(70)
        super()._set_vampirism(0.15)

        self.__max_points = 0
        self.__level = 0
        self.__points = 0
        self.__timer = 1000

    def post_attack(self, hero, ack, result):
        if self.__level == 0:
            self.__level = hero.stats["level"]
            self.__max_points = 400 + ((self.__level - 1) * 400 / 11)
            self.__points = self.__max_points
        if self.__timer == 0:
            self.__timer = 1000
            self.__points = min(self.__points + (self.__max_points / 120), self.__max_points)
        else:
            self.__timer -= 1
        if ack["on_hero"]:
            if self.__points:
                if self.__points - ack["wp_dmg"] < 0:
                    recover = (0.25 * self.__points) + (hero.stats["vampirism"] * (ack["wp_dmg"] - self.__points))
                    self.__points = 0
                else:
                    self.__points -= ack["wp_dmg"]
                    recover = 0.25 * ack["wp_dmg"]
                result["recover"] = recover
        else:
            result["recover"] = ack["wp_dmg"] * hero.stats["vampirism"]
        return result


class SixSins(Item):
    def __init__(self):
        super().__init__("Six Sins")
        super()._set_wp(25)


class SorrowBlade(Item):
    def __init__(self):
        super().__init__("Sorrow Blade")
        super()._set_wp(120)


class Spellsword(Item):
    def __init__(self):
        super().__init__("Spellsword")
        super()._set_wp(85)
        super()._set_cooldown(0.2)
        super()._set_energy_regen(2)

    @staticmethod
    def on_attack(hero, the_attack):
        if the_attack["hit"]:
            hero.stats["energy"] = max(hero.stats["base_energy"],
                                       hero.stats["energy"] + (12 if the_attack["on_hero"] else 4))
        return the_attack


class SwiftShooter(Item):
    def __init__(self):
        super().__init__("Swift Shooter")
        super()._set_bonus_as(0.1)


class TensionBow(Item):
    def __init__(self):
        super().__init__("Tension Bow")
        super()._set_wp(40)
        super()._set_armor_peirce(0.3)
        self.__timer = 0

    def on_attack(self, hero, the_attack):
        if the_attack["hit"] and self.__timer == 0:
            self.__timer = 6000
            the_attack["wp_dmg"] += 100 + hero.stats["wp"]
        return the_attack

    def post_attack(self, hero, ack, result):
        if self.__timer > 0:
            self.__timer -= 1
        return result

class TornadoTrigger(Item):
    def __init__(self):
        super().__init__("Tornado Trigger")
        super()._set_bonus_as(0.4)
        super()._set_crit_chance(0.35)
        super()._set_crit_damage(0.05)

        self.__buff_speed_time = 0

    def on_attack(self, hero, the_attack):
        if the_attack["hit"] and the_attack["with_basic"] and the_attack["on_hero"]:
            self.__buff_speed_time = 1200
            hero.stats["move_speed"] += 0.1 * hero.stats["base_move_speed"]
        return the_attack

    def post_attack(self, hero, ack, result):
        if self.__buff_speed_time > 0:
            self.__buff_speed_time -= 1
        else:
            hero.stats["move_speed"] = hero.stats["base_move_speed"]
        return result


class TyrantsMonocle(Item):
    def __init__(self):
        super().__init__("Tyrants Monocle")
        super()._set_wp(60)
        super()._set_crit_damage(0.15)
        super()._set_crit_chance(0.35)


class WeaponBlade(Item):
    def __init__(self):
        super().__init__("Weapon Blade")
        super()._set_wp(10)


# Start of Defense Tree
class Aegis(Item):
    def __init__(self):
        super().__init__("Aegis")
        super()._set_shield(45)
        super()._set_armor(45)
        super()._set_bonus_hp(200)
        self.warn("i-a", "ACTIVE EFFECT triggers when available to block stun or silence. May not be optimal.")
        self.__cooldown = 0
        self.__is_active = False
        self.__active_time = 1500

    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        barrier = 100 + (500 * (hero.stats["level"] - 1) / 11)
        if self.__is_active:
            ack["prevent_cc"] = True
        if pre_dmg:
            if (the_attack["stun"] or the_attack["silence"]) and not self.__cooldown:
                hero.stats["bonus_hp"] += barrier
                self.__is_active = True
                self.__cooldown = 45000
                self.__active_time = 1500
        else:
            if self.__is_active:
                self.__active_time -= 1
            if not self.__active_time:
                self.__is_active = False
                hero.stats["bonus_hp"] -= barrier
                self.__active_time = 1500
            if self.__cooldown:
                self.__cooldown -= 1
        return ack


class AtlasPauldron(Item):
    def __init__(self):
        super().__init__("Atlas Pauldron")
        super()._set_armor(65)
         # TODO: Activate: Maim nearby enemies, lowering their attack speed by 50% of their total for 4s in a 5-meter range. Additionally reduces weapon power damage by 30%. (45s cooldown)
        self.warn("i-a", "ACTIVE EFFECT either not implemented or considered in combat. May skew results.")


class CapacitorPlate(Item):
    def __init__(self):
        super().__init__("Capacitor Plate")
        super()._set_shield(30)
        super()._set_armor(30)
        super()._set_bonus_hp(450)
        super()._set_cooldown(0.15)
        # TODO: Passive: Your heals and barriers are 15% stronger. Passive: Your heals and barriers also grant other allied heroes bonus movement speed for 3s. (15s cooldown per hero)
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")


class CelestialShroud(Item):
    def __init__(self):
        super().__init__("Celestial Shroud")
        super()._set_shield(95)
        super()._set_bonus_hp(300)
        self.__cooldown = 0
        self.__is_active = False
        self.__active_time = 1500

    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        if self.__is_active:
            ack["prevent_cc"] = True
        if pre_dmg:
            if not the_attack["with_basic"] and not self.__cooldown:
                self.__is_active = True
                self.__cooldown = 35000
                self.__active_time = 500
        else:
            if self.__is_active:
                self.__active_time -= 1
            if not self.__active_time:
                self.__is_active = False
                self.__active_time = 500
            if self.__cooldown:
                self.__cooldown -= 1
        return ack



class CoatofPlates(Item):
    def __init__(self):
        super().__init__("Coat of Plates")
        super()._set_armor(55)


class Crucible(Item):
    def __init__(self):
        super().__init__("Crucible")
        super()._set_bonus_hp(550)
        self.warn("i-a", "ACTIVE EFFECT triggers when available to block stun or silence. Since 1v1, this behaves exactly like reflex block. May not be optimal.")
        self.__cooldown = 0
        self.__is_active = False
        self.__active_time = 1500

    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        barrier = 100 + (500 * (hero.stats["level"] - 1) / 11)
        if self.__is_active:
            ack["prevent_cc"] = True
        if pre_dmg:
            if (the_attack["stun"] or the_attack["silence"]) and not self.__cooldown:
                hero.stats["bonus_hp"] += barrier
                self.__is_active = True
                self.__cooldown = 75000
                self.__active_time = 1500
        else:
            if self.__is_active:
                self.__active_time -= 1
            if not self.__active_time:
                self.__is_active = False
                hero.stats["bonus_hp"] -= barrier
                self.__active_time = 1500
            if self.__cooldown:
                self.__cooldown -= 1
        return ack


class Dragonheart(Item):
    def __init__(self):
        super().__init__("Dragonheart")
        super()._set_bonus_hp(350)


class FountainOfRenewal(Item):
    def __init__(self):
        super().__init__("Fountain of Renewal")
        super()._set_bonus_hp(400)
        super()._set_shield(40)
        super()._set_armor(40)
        self.warn("i-a", "ACTIVE EFFECT trigger at 25% or less health. Does not help teammates (1v1 situation). May not be optimal.")
        self.__combat_timer = 0
        self.__normal_hp_regen = -1
        self.__set = False
        self.__threshold = 0.25
        self.__cooldown = 0
        self.__is_active = False
        self.__active_duration = 0

    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        if self.__threshold >= hero.stats["current_hp"] / (hero.stats["base_hp"] + hero.stats["bonus_hp"]):
            if not self.__cooldown:
                self.__is_active = True
                self.__active_duration = 3000
                self.__cooldown = 75000
        if pre_dmg:
            if self.__combat_timer:
                self.__combat_timer -= 1
            if not self.__combat_timer:
                if not self.__set:
                    self.__normal_hp_regen = hero.stats["hp_regen"]
                    self.__set = True
                hero.stats["hp_regen"] = 0.015
            if the_attack["hit"]:
                self.__combat_timer = 5000
                hero.stats["hp_regen"] = self.__normal_hp_regen
        return ack

    def post_attack(self, hero, ack, result):
        if self.__is_active and (self.__active_duration % 1000 == 0):
            result["recover"] += 250 * (1 - (hero.stats["current_hp"] / (hero.stats["base_hp"] + hero.stats["bonus_hp"])))
        if self.__active_duration:
            self.__active_duration -= 1
        if self.__cooldown:
            self.__cooldown -= 1
        if not self.__active_duration:
            self.__is_active = False
        return result


class KineticShield(Item):
    def __init__(self):
        super().__init__("Kinetic Shield")
        super()._set_shield(55)


class Lifespring(Item):
    def __init__(self):
        super().__init__("Lifespring")
        super()._set_bonus_hp(200)
        self.__combat_timer = 0
        self.__normal_hp_regen = -1
        self.__set = False

    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        if pre_dmg:
            if self.__combat_timer:
                self.__combat_timer -= 1
            if not self.__combat_timer:
                if not self.__set:
                    self.__normal_hp_regen = hero.stats["hp_regen"]
                    self.__set = True
                hero.stats["hp_regen"] = 0.015
            if the_attack["hit"]:
                self.__combat_timer = 5000
                hero.stats["hp_regen"] = self.__normal_hp_regen
        return ack


class LightArmor(Item):
    def __init__(self):
        super().__init__("Light Armor")
        super()._set_armor(25)


class LightShield(Item):
    def __init__(self):
        super().__init__("Light Shield")
        super()._set_shield(25)


class MetalJacket(Item):
    def __init__(self):
        super().__init__("Metal Jacket")
        super()._set_armor(95)
        self.warn("i-i",
                  "unclear when the PASSIVE EFFECT is supposed to be considered/if affects true damage."
                  " Assuming damage reduction from the passive includes true damage and is considered "
                  "right before taking the damage. May skew results.")

    @staticmethod
    def on_damage_receive(hero, ack, the_attack, pre_dmg=True):
        if the_attack["with_basic"] and pre_dmg:
            ack["true_dmg"] *= 0.85
            ack["cp_dmg"] *= 0.85
            ack["wp_dmg"] *= 0.85
        return ack


class Oakheart(Item):
    def __init__(self):
        super().__init__("Oakheart")
        super()._set_bonus_hp(150)


class Pulseweave(Item):
    def __init__(self):
        super().__init__("Pulseweave")
        super()._set_bonus_hp(600)
        super()._set_move_speed_ratio(0.08)
        self.warn("i-p", "Current state of program assumes that heroes are right next to each other, maximizing the damage of this item. May skew results.")
        self.warn("i-i", "'Sprint' active is not well documented. Assumes +2 move speed.")
        self.__is_available = True
        self.__is_active = False
        self.__cooldown = 0
        self.__duration = 0
        self.__pulse_timer = 0
        self.__burst = False
        self.__combat_timer = 0
        self.__normal_hp_regen = -1
        self.__set = False
    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        if pre_dmg:
            if self.__is_available and the_attack["hit"]:
                self.__is_active = True
                self.__is_available = False
                self.__cooldown = 45000
                hero.stats["move_speed"] += 2
                self.__duration = 3000
                if self.__combat_timer:
                    self.__combat_timer -= 1
                if not self.__combat_timer:
                    if not self.__set:
                        self.__normal_hp_regen = hero.stats["hp_regen"]
                        self.__set = True
                    hero.stats["hp_regen"] = 0.015
                if the_attack["hit"]:
                    self.__combat_timer = 5000
                    hero.stats["hp_regen"] = self.__normal_hp_regen
        else:
            if self.__duration == 1:
                self.__burst = True
            if self.__cooldown:
                self.__cooldown -= 1
            if not self.__cooldown:
                self.__is_available = True
            if self.__duration:
                self.__duration -= 1
            if not self.__duration:
                self.__is_active = False
                hero.stats["move_speed"] -= 2
            if not the_attack["hit"]:
                if self.__combat_timer:
                    self.__combat_timer -= 1
                elif self.__timer:
                    self.__timer -= 1
                if not self.__timer and not self.__combat_timer:
                    self.__normal_hp_regen = hero.stats["hp_regen"]
                    hero.stats["hp_regen"] += 0.015
            else:
                self.__combat_timer = 5000
                self.__timer = 1000
                hero.stats["hp_regen"] = self.__normal_hp_regen
        return ack

    def on_attack(self, hero, the_attack):
        pulse_dmg = 50 + (0.15 * hero.stats["bonus_hp"])
        if self.__pulse_timer:
            self.__pulse_timer -= 1
        else:
            self.__pulse_timer = 1000
            if self.__is_available:
                the_attack["cp_dmg"] += pulse_dmg / 2
        if self.__burst:
            the_attack["cp_dmg"] += pulse_dmg
            the_attack["slow"] = 0.05
            the_attack["slow_duration"] = 3000
            self.__burst = False
        return the_attack


class ProtectorContract(Item):
    def __init__(self):
        super().__init__("Protector Contract")
        super()._set_bonus_hp(300)
        # TODO: Passive: After using an ability, your next basic attack against an enemy hero will grant 150 barrier to nearby allies for 2s. (12s cooldown)
        self.warn("i-p", "PASSIVE EFFECT relies on ability use and only affects teammates - neither of which a current feature - and thus is not implemented or activated. May skew results.")

class ReflexBlock(Item):
    def __init__(self):
        super().__init__("Reflex Block")
        super()._set_bonus_hp(150)
        self.warn("i-a", "ACTIVE EFFECT triggers when available to block stun or silence. May not be optimal.")
        self.__cooldown = 0
        self.__is_active = False
        self.__active_time = 1500


    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        barrier = 100 + (500 * (hero.stats["level"] - 1) / 11)
        if self.__is_active:
            ack["prevent_cc"] = True
        if pre_dmg:
            if (the_attack["stun"] or the_attack["silence"]) and not self.__cooldown:
                hero.stats["bonus_hp"] += barrier
                self.__is_active = True
                self.__cooldown = 90000
                self.__active_time = 1500
        else:
            if self.__is_active:
                self.__active_time -= 1
            if not self.__active_time:
                self.__is_active = False
                hero.stats["bonus_hp"] -= barrier
                self.__active_time = 1500
            if self.__cooldown:
                self.__cooldown -= 1
        return ack




class RooksDecree(Item):
    def __init__(self):
        super().__init__("Rook's Decree")
        super()._set_bonus_hp(550)
        super()._set_armor(30)
        super()._set_shield(30)
        super()._set_cooldown(0.05)
        # TODO: Passive: After using an ability, your next basic attack against an enemy hero applies a barrier (150 + 15% of bonus health) to all nearby allies for 2 seconds (10s cooldown).
        self.warn("i-p", "PASSIVE EFFECT relies on ability use and only affects teammates - neither of which a current feature - and thus is not implemented or activated. May skew results.")


class SlumberingHusk(Item):
    def __init__(self):
        super().__init__("Slumbering Husk")
        super()._set_armor(55)
        super()._set_shield(55)
        self.__cooldown = 0
        self.__effect_active = False
        self.__effect_timer = 2000
        self.__dmg_timer = 0
        self.__hero_hp_for_timer = 0


    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        if pre_dmg:
            if not self.__cooldown:
                if not self.__dmg_timer:
                    self.__hero_hp_for_timer = hero.stats["current_hp"]
                    self.__dmg_timer = 1000
            return ack

        if not self.__cooldown:
            if 0.25 <= ((self.__hero_hp_for_timer - hero.stats["current_hp"]) / hero.stats["base_hp"]):
                self.__effect_active = True
                self.__cooldown = 30000
            if self.__dmg_timer:
                self.__dmg_timer -= 1
        else:
            self.__cooldown -= 1
        if self.__effect_active:
            if self.__effect_timer == 2000:
                hero.stats["current_hp"] *= 2
                hero.stats["base_hp"] *= 2
            self.__effect_timer -= 1
        if not self.__effect_timer:
            hero.stats["current_hp"] /= 2
            hero.stats["base_hp"] /= 2
            self.__effect_active = False
            self.__effect_timer = 2000
        return ack


class Warmail(Item):
    def __init__(self):
        super().__init__("Warmail")
        super()._set_armor(30)
        super()._set_shield(30)