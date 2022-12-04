class Item:
    def __init__(self, name, hp_buff, hp_regen_buff, energy_buff, energy_regen_buff, wp_buff, cp_buff, as_buff, crit_chance, crit_damage, cooldown, move_speed_buff, vampirism, armor_peirce, shield_perice):
        self.name = name
        self.changes = {
            "base_hp": hp_buff,
            "hp_regen": hp_regen_buff,
            "energy": energy_buff,
            "energy_regen": energy_regen_buff,
            "wp": wp_buff,
            "cp": cp_buff,
            "as": as_buff,
            "move_speed": move_speed_buff,
            "crit_chance": crit_chance,
            "crit_damage": crit_damage,
            "vampirism": vampirism,
            "cooldown": cooldown,
            "armor_peirce": armor_peirce,
            "shield_peirce": shield_perice,
            "item_passives": dict(),
            "item_actives": dict()
        }


class SorrowBlade(Item):
    def __init__(self):
        super().__init__("Sorrow Blade", 0, 0, 0, 0, 125, 0, 0, 0.0, 0.0, 0, 0.0, 0, 0, 0)


class TornadoTrigger(Item):
    def __init__(self):
        super().__init__("Tornado Trigger", 0, 0, 0, 0, 0, 0, 0.4, 0.35, 0.05, 0.0, 0.0, 0.0, 0, 0)
        self._get_passives()

    def _get_passives(self):
        self.changes["item_passives"] = list() # TODO


class TyrantsMonocle(Item):
    def __init__(self):
        super().__init__("Tyrants Monocle", 0, 0, 0, 0, 50, 0, 0, 0.35, 0.15, 0.0, 0.0, 0.0, 0, 0)


class PoisonedShiv(Item):
    def __init__(self):
        super().__init__("Poisoned Shiv", 0, 0, 0, 0, 35, 0, 0.35, 0.0, 0.0, 0.0, 0.0, 0.1, 0, 0)
        self._get_passives()

    def _get_passives(self):
        self.changes["item_passives"] = list()  # TODO


class BoneSaw(Item):
    def __init__(self):
        super().__init__("Poisoned Shiv", 0, 0, 0, 0, 30, 0, 0.3, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2, 0)
        self._get_passives()

    def _get_passives(self):
        self.changes["item_passives"] = list()  # TODO
