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

class SorrowBlade(Item):
    def __init__(self):
        super().__init__("Sorrow Blade")
        super()._set_wp(125)


class TornadoTrigger(Item):
    def __init__(self):
        super().__init__("Tornado Trigger")
        super()._set_bonus_as(0.4)
        super()._set_crit_chance(0.35)
        super()._set_crit_damage(0.05)

        self.changes["item_passives"] = {
            self.name: self.__passives
        }
        self.__buff_speed_time = 0

    def __passives(self, hero, hit):
        if hit:
            self.__buff_speed_time = 1200
            hero.stats["move_speed"] += 0.1 * hero.stats["base_move_speed"]
        elif self.__buff_speed_time > 0:
            self.__buff_speed_time -= 1
            if self.__buff_speed_time == 0:
                hero.stats["move_speed"] = hero.stats["base_move_speed"]


class TyrantsMonocle(Item):
    def __init__(self):
        super().__init__("Tyrants Monocle")
        super()._set_wp(50)
        super()._set_crit_damage(0.15)
        super()._set_crit_chance(0.35)


class PoisonedShiv(Item):
    def __init__(self):
        super().__init__("Poisoned Shiv")
        super()._set_wp(35)
        super()._set_bonus_as(0.35)
        super()._set_vampirism(0.1)

        self.changes["item_passives"] = {
            self.name: self._passives
        }
        self.__hit_num_odd = False

    def _passives(self, hero, kill_minion=False, with_basic=False):
        if kill_minion:
            hero.stats["current_hp"] += 25 if with_basic else 10
        self.__hit_num_odd = not self.__hit_num_odd
        return 1200 if not self.__hit_num_odd else 0


class BoneSaw(Item):
    def __init__(self):
        super().__init__("Bone Saw")
        super()._set_wp(30)
        super()._set_armor_peirce(0.2)
        super()._set_bonus_as(0.3)

        self.changes["item_passives"] = {
            self.name: self._passives
        }
        self.__stacks = 0
        self.__timer = 0

    def _passives(self, hit):
        if hit:
            self.__stacks = min(self.__stacks + 1, 5)
            self.__timer = 3000
        elif self.__timer > 0:
            self.__timer -= 1
        if self.__timer == 0 and self.__stacks > 0:
            self.__stacks -= 1
            self.__timer = 100 # not accurate cuz am lazy. real implementation would count time between attacks
        return self.__stacks * 0.1


class BarbedNeedle(Item):
    def __init__(self):
        super().__init__("Barbed Needle")
        super()._set_wp(10)
        super()._set_vampirism(0.1)

        self.changes["item_passives"] = {
            self.name: self._passives
        }

    @staticmethod
    def _passives(hero, kill_minion=False, with_basic=False):
        if kill_minion:
            hero.stats["current_hp"] += 25 if with_basic else 10


class BlazingSalvo(Item):
    def __init__(self):
        super().__init__("Blazing Salvo")
        super()._set_bonus_as(0.2)


class SwiftShooter(Item):
    def __init__(self):
        super().__init__("Swift Shooter")
        super()._set_bonus_as(0.1)

class BookOfEulogies(Item):
    def __init__(self):
        super().__init__("Book of Eulogies")
        super()._set_wp(5)
        super()._set_vampirism(0.05)

        self.changes["item_passives"] = {
            self.name: self._passives
        }

    def _passives(self, hero, kill_minion=False, with_basic=False):
        if kill_minion:
            hero.stats["current_hp"] += 25 if with_basic else 10


class BreakingPoint(Item):
    def __init__(self):
        super().__init__("Breaking Point")
        super()._set_wp(50)
        super()._set_bonus_as(0.2)

        self.changes["item_passives"] = {
            self.name: self._passives
        }
        self.__stacks = 0
        self.__timer = 0
        self.__leftover = 0

    def _passives(self, hero, hit, damage_done=0):
        if hit:
            self.__timer = 2500
            if damage_done == 0:
                return 5 * self.__stacks
            damage_done += self.__leftover
            while True:
                dmg_needed = 100 + self.__stacks * (5 if hero.stats["ismelee"] else 10)
                if damage_done >= dmg_needed:
                    if self.__stacks < 35:
                        self.__stacks += 1
                    damage_done -= dmg_needed
                else:
                    self.__leftover = damage_done
                    break
        elif self.__timer > 0:
            self.__timer -= 1
        else:
            self.__stacks -= 1
            self.__timer = 200


class HeavySteel(Item):
    def __init__(self):
        super().__init__("Heavy Steel")
        super()._set_wp(45)


class WeaponBlade(Item):
    def __init__(self):
        super().__init__("Weapon Blade")
        super()._set_wp(10)


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

        self.changes["item_passives"] = {
            self.name: self._passives
        }
        self.__is_first = True

    def _passives(self, hero):
        if self.__is_first:
            self._normal_crit_perc = hero.stats["crit_chance"]
            hero.stats["crit_chance"] = 1.0
        else:
            hero.stats["crit_chance"] = self._normal_crit_perc


class PiercingSpear(Item):
    def __init__(self):
        super().__init__("Piercing Spear")
        super()._set_wp(15)
        super()._set_armor_peirce(0.1)


class SerpentMask(Item):
    def __init__(self):
        super().__init__("Serpent Mask")
        super()._set_wp(70)
        super()._set_vampirism(0.15)

        self.changes["item_passives"] = {
            self.name: self._passives
        }
        self.__max_points = 0
        self.__level = 0
        self.__points = 0
        self.__timer = 1000

    def _passives(self, hero, dmg):
        if self.__level == 0:
            self.__level = hero.stats["level"]
            self.__max_points = 400 + ((self.__level - 1) * 400 / 11)
            self.__points = self.__max_points
        if self.__timer == 0:
            self.__timer = 1000
            self.__points = min(self.__points + (self.__max_points / 40), self.__max_points)
        else:
            self.__timer -= 1
        if self.__points:
            if self.__points - dmg < 0:
                tmp = self.__points
                self.__points = 0
                return 0.25 * self.__points, dmg - tmp
            else:
                self.__points -= dmg
                return 0.25 * dmg, 0
        return 0, 0


class SixSins(Item):
    def __init__(self):
        super().__init__("Six Sins")
        super()._set_wp(25)


class Spellsword(Item):
    def __init__(self):
        super().__init__("Spellsword")
        super()._set_wp(85)
        super()._set_cooldown(0.35)
        super()._set_energy_regen(2)

        self.changes["item_passives"] = {
            self.name: self._passives
        }

    @staticmethod
    def _passives(hero, on_hero=True):
        hero.stats["energy"] = max(hero.stats["base_energy"], hero.stats["energy"] + (12 if on_hero else 4))


class TensionBow(Item):
    def __init__(self):
        super().__init__("Tension Bow")
        super()._set_wp(40)
        super()._set_armor_peirce(0.3)

        self.changes["item_passives"] = {
            self.name: self._passives
        }
        self.__timer = 0

    def _passives(self, hero, hit):
        if hit and self.__timer == 0:
            self.__timer = 6000
            return 100 + hero.stats["wp"]
        elif self.__timer > 0:
            self.__timer -= 1
        return 0
