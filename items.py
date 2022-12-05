class Item:
    def __init__(self, name, hp_buff, hp_regen_buff, energy_buff, energy_regen_buff, wp_buff, cp_buff, as_buff, crit_chance, crit_damage, cooldown, move_speed_buff, vampirism, armor_peirce, shield_perice, crystal_lifesteal):
        self.name = name
        self.changes = {
            "base_hp": hp_buff,
            "hp_regen": hp_regen_buff,
            "base_energy": energy_buff,
            "energy_regen": energy_regen_buff,
            "wp": wp_buff,
            "cp": cp_buff,
            "bonus_as": as_buff,
            "move_speed": move_speed_buff,
            "crit_chance": crit_chance,
            "crit_damage": crit_damage,
            "vampirism": vampirism,
            "cooldown": cooldown,
            "armor_peirce": armor_peirce,
            "shield_peirce": shield_perice,
            "item_passives": dict(),
            "item_actives": dict(),
            "crystal_lifesteal": crystal_lifesteal
        }


class SorrowBlade(Item):
    def __init__(self):
        super().__init__("Sorrow Blade", 0, 0, 0, 0, 125, 0, 0, 0.0, 0.0, 0, 0.0, 0, 0, 0, 0)


class TornadoTrigger(Item):
    def __init__(self):
        super().__init__("Tornado Trigger", 0, 0, 0, 0, 0, 0, 0.4, 0.35, 0.05, 0.0, 0.0, 0.0, 0, 0, 0)
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
        super().__init__("Tyrants Monocle", 0, 0, 0, 0, 50, 0, 0, 0.35, 0.15, 0.0, 0.0, 0.0, 0, 0, 0)


class PoisonedShiv(Item):
    def __init__(self):
        super().__init__("Poisoned Shiv", 0, 0, 0, 0, 35, 0, 0.35, 0.0, 0.0, 0.0, 0.0, 0.1, 0, 0, 0)
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
        super().__init__("Bone Saw", 0, 0, 0, 0, 30, 0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0, 0)
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
        super().__init__("Barbed Needle", 0, 0, 0, 0, 10, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0, 0, 0)
        self.changes["item_passives"] = {
            self.name: self._passives
        }

    @staticmethod
    def _passives(hero, kill_minion=False, with_basic=False):
        if kill_minion:
            hero.stats["current_hp"] += 25 if with_basic else 10


class BlazingSalvo(Item):
    def __init__(self):
        super().__init__("Blazing Salvo", 0, 0, 0, 0, 0, 0, 0.2, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0)


class SwiftShooter(Item):
    def __init__(self):
        super().__init__("Swift Shooter", 0, 0, 0, 0, 0, 0, 0.1, 0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0)


class BookOfEulogies(Item):
    def __init__(self):
        super().__init__("Book of Eulogies", 0, 0, 0, 0, 5, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.05, 0, 0, 0)
        self.changes["item_passives"] = {
            self.name: self._passives
        }

    def _passives(self, hero, kill_minion=False, with_basic=False):
        if kill_minion:
            hero.stats["current_hp"] += 25 if with_basic else 10


class BreakingPoint(Item):
    def __init__(self):
        super().__init__("Breaking Point", 0, 0, 0, 0, 50, 0, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0)
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
        super().__init__("Heavy Steel", 0, 0, 0, 0, 45, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0)


class WeaponBlade(Item):
    def __init__(self):
        super().__init__("Weapon Blade", 0, 0, 0, 0, 10, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0)


class LuckyStrike(Item):
    def __init__(self):
        super().__init__("Lucky Strike", 0, 0, 0, 0, 0, 0, 0.0, 0.2, 0.05, 0.0, 0.0, 0.0, 0, 0, 0)


class MinionsFoot(Item):
    def __init__(self):
        super().__init__("Minion's Foot", 0, 0, 0, 0, 0, 0, 0.0, 0.1, 0.05, 0.0, 0.0, 0.0, 0, 0, 0)
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
        super().__init__("Piercing Spear", 0, 0, 0, 0, 15, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0, 0)


class SerpentMask(Item):
    def __init__(self):
        super().__init__("Serpent Mask", 0, 0, 0, 0, 70, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.15, 0, 0, 0)
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
            self.__max_points = 400 + (self.__level * 400 / 11)
            self.__points = self.__max_points
        if self.__timer == 0:
            self.__timer = 1000
            self.__points = min(self.__points + self.__max_points / 40, self.__max_points)
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
        super().__init__("Six Sins", 0, 0, 0, 0, 25, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 0)


class Spellsword(Item):
    def __init__(self):
        super().__init__("Spellsword", 0, 0, 0, 2, 85, 0, 0.0, 0.0, 0.35, 0.0, 0.0, 0.0, 0, 0, 0)
        self.changes["item_passives"] = {
            self.name: self._passives
        }

    @staticmethod
    def _passives(hero, on_hero=True):
        hero.stats["energy"] = max(hero.stats["base_energy"], hero.stats["energy"] + (12 if on_hero else 4))


class TensionBow(Item):
    def __init__(self):
        super().__init__("Tension Bow", 0, 0, 0, 0, 40, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0, 0)
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
