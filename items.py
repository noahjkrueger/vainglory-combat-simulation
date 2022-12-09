class Item:
    def __init__(self, name):
        self.name = name
        self.changes = dict()

    def _set_base_hp(self, val):
        self.changes["base_hp"] = val

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
    def post_basic(hero, ack, result):
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
        self.warn("i-i", "once decay is active (after 3s delay), stacks drop ever .1s instead of 3s from hit. Negligible but may skew results.")

    def on_attack(self, hero, the_attack):
        if the_attack["hit"] and the_attack["with_basic"]:
            self.__stacks = min(self.__stacks + 1, 5)
            self.__timer = 3000
        the_attack["armor_peirce"] = max(self.__stacks * 0.1 + the_attack["armor_peirce"], the_attack["armor_peirce"])
        return the_attack

    def post_basic(self, hero, ack, result):
        if self.__timer > 0:
            self.__timer -= 1
        if self.__timer == 0 and self.__stacks > 0:
            self.__stacks -= 1
            self.__timer = 100 # not accurate cuz am lazy. real implementation would count time between attacks
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
    def post_basic(hero, ack, result):
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

    def post_basic(self, hero, ack, result):
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
    def post_basic(hero, ack, result):
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

    def post_basic(self, hero, ack, result):
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

    def post_basic(self, hero, ack, result):
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

    def post_basic(self, hero, ack, result):
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
        super()._set_base_hp(200)
        # TODO: Activate: Reflex Block (45s cooldown)
        self.warn("i-a", "ACTIVE EFFECT either not implemented or considered in combat. May skew results.")


class AtlasPauldron(Item):
    def __init__(self):
        super().__init__("Atlas Pauldron")
        super()._set_armor(65)
         # TODO: Activate: Maim nearby enemies, lowering their attack speed by 50% of their total for 4s in a 5-meter range. Additionaly reduces weapon power damage by 30%. (45s cooldown)
        self.warn("i-a", "ACTIVE EFFECT either not implemented or considered in combat. May skew results.")


class CapacitorPlate(Item):
    def __init__(self):
        super().__init__("Capacitor Plate")
        super()._set_shield(30)
        super()._set_armor(30)
        super()._set_base_hp(450)
        super()._set_cooldown(0.15)
        # TODO: Passive: Your heals and barriers are 15% stronger. Passive: Your heals and barriers also grant other allied heroes bonus movement speed for 3s. (15s cooldown per hero)
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")


class CelestialShroud(Item):
    def __init__(self):
        super().__init__("Celestial Shroud")
        super()._set_shield(95)
        super()._set_base_hp(300)
        # TODO: Passive: Grants immunity to abilities and damaging debuffs. Disabled for 35s shortly after negating ability damage.
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")



class CoatofPlates(Item):
    def __init__(self):
        super().__init__("Coat of Plates")
        super()._set_armor(55)


class Crucible(Item):
    def __init__(self):
        super().__init__("Crucible")
        super()._set_base_hp(550)
        # TODO: Activate: Trigger Reflex Block for you and nearby teammates. (75s cooldown)
        self.warn("i-a", "ACTIVE EFFECT either not implemented or considered in combat. May skew results.")


class Dragonheart(Item):
    def __init__(self):
        super().__init__("Dragonheart")
        super()._set_base_hp(350)


class FountainOfRenewal(Item):
    def __init__(self):
        super().__init__("Fountain of Renewal")
        super()._set_base_hp(400)
        super()._set_shield(40)
        super()._set_armor(40)
        # TODO: Passive: Lifespring Activate: Heals you and nearby allies for 2.5 health for each % missing health per second for 3s. (75s cooldown)
        self.warn("i-a", "ACTIVE EFFECT either not implemented or considered in combat. May skew results.")
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")


class KineticShield(Item):
    def __init__(self):
        super().__init__("Kinetic Shield")
        super()._set_shield(55)


class Lifespring(Item):
    def __init__(self):
        super().__init__("Lifespring")
        super()._set_base_hp(200)
        # TODO: Passive: Regenerate 1.5% of your missing health per second whenever you are out of combat with enemy heroes for 5s.
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")


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
        # TODO: Passive: Reduces incoming damage from Basic Attacks by 15%.
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")

    def on_damage_receive(self, hero, ack, the_attack, pre_dmg=True):
        if the_attack["with_basic"]:
            ack["true_dmg"] *= 0.85
            ack["cp_dmg"] *= 0.85
            ack["wp_dmg"] *= 0.85

class Oakheart(Item):
    def __init__(self):
        super().__init__("Oakheart")
        super()._set_base_hp(150)


class Pulseweave(Item):
    def __init__(self):
        super().__init__("Pulseweave")
        super()._set_base_hp(600)
        # TODO: Passive: Upon taking damage from an enemy hero, gain bonus movement speed for 3s then deal 50
        #  (+15% of bonus health) damage and slow enemies by 5% (+0.03% of bonus health) for 3s. Also deals 50%
        #  of the burst damage per second to nearby enemies while available. (45s cooldown) Passive: +8% base
        #  movement speed Passive: Lifespring
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")


class ProtectorContract(Item):
    def __init__(self):
        super().__init__("Protector Contract")
        super()._set_base_hp(300)
        #TODO: Passive: After using an ability, your next basic attack against an enemy hero will grant 150 barrier to nearby allies for 2s. (12s cooldown)
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")

class ReflexBlock(Item):
    def __init__(self):
        super().__init__("Reflex Block")
        super()._set_base_hp(150)
        # TODO: Activate: Gain a barrier worth 100-600 (level 1-12) and block all debuffs for 1.5s. (90s cooldown)
        self.warn("i-a", "ACTIVE EFFECT either not implemented or considered in combat. May skew results.")


class RooksDecree(Item):
    def __init__(self):
        super().__init__("Rook's Decree")
        super()._set_base_hp(550)
        super()._set_armor(30)
        super()._set_shield(30)
        super()._set_cooldown(0.05)
        # TODO: Passive: After using an ability, your next basic attack against an enemy hero applies a barrier (150 + 15% of bonus health) to all nearby allies for 2 seconds (10s cooldown).
        self.warn("i-p", "PASSIVE EFFECT either not implemented or considered in combat. May skew results.")
        self.warn("i-a", "PASSIVE EFFECT relies on ability use - not a current feature - and will not be activated. May skew results.")

    # def on_attack(self):

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