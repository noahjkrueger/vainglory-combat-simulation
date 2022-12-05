import matplotlib.pyplot as plt
import heroes, items
from sys import argv
import argparse


def create_item(item):
    if item.upper() == "SORROWBLADE":
        return items.SorrowBlade()
    elif item.upper() == "TYRANTSMONOCLE":
        return items.TyrantsMonocle()
    elif item.upper() == "TORNADOTRIGGER":
        return items.TornadoTrigger()
    elif item.upper() == "POISONEDSHIV":
        return items.PoisonedShiv()
    elif item.upper() == "BONESAW":
        return items.BoneSaw()
    elif item.upper() == "SPELLSWORD":
        return items.Spellsword()
    elif item.upper() == "SIXSINS":
        return items.SixSins()
    elif item.upper() == "SERPENTMASK":
        return items.SerpentMask()
    elif item.upper() == "SWIFTSHOOTER":
        return items.SwiftShooter()
    elif item.upper() == "BLAZINGSALVO":
        return items.BlazingSalvo()
    elif item.upper() == "HEAVYSTEEL":
        return items.HeavySteel()
    elif item.upper() == "LUCKYSTRIKE":
        return items.LuckyStrike()
    elif item.upper() == "PIERCINGSPEAR":
        return items.PiercingSpear()
    elif item.upper() == "BOOKOFEULOGIES":
        return items.BookOfEulogies()
    elif item.upper() == "MINIONSFOOT":
        return items.MinionsFoot()
    elif item.upper() == "TENSIONBOW":
        return items.TensionBow()
    elif item.upper() == "BARBEDNEEDLE":
        return items.BarbedNeedle()
    elif item.upper() == "BREAKINGPOINT":
        return items.BreakingPoint()
    elif item.upper() == "WEAPONBLADE":
        return items.WeaponBlade()
    else:
        raise Exception(f"Invalid item name '{item}' - misspelling, malformed or not implemented")

def create_hero(hero_name, level, stutter):
    if hero_name.upper() == "AMAEL":
        return heroes.Amael(level, stutter)
    elif hero_name.upper() == "ADAGIO":
        return heroes.Adagio(level, stutter)
    elif hero_name.upper() == "ALPHA":
        return heroes.Alpha(level, stutter)
    elif hero_name.upper() == "ANKA":
        return heroes.Anka(level, stutter)
    elif hero_name.upper() == "ARDAN":
        return heroes.Ardan(level, stutter)
    elif hero_name.upper() == "BAPTISTE":
        return heroes.Baptiste(level, stutter)
    elif hero_name.upper() == "BARON":
        return heroes.Baron(level, stutter)
    elif hero_name.upper() == "BLACKFEATHER":
        return heroes.Blackfeather(level, stutter)
    elif hero_name.upper() == "CAINE":
        return heroes.Caine(level, stutter)
    elif hero_name.upper() == "CATHERINE":
        return heroes.Catherine(level, stutter)
    elif hero_name.upper() == "CELESTE":
        return heroes.Celeste(level, stutter)
    elif hero_name.upper() == "CHURNWALKER":
        return heroes.Churnwalker(level, stutter)
    elif hero_name.upper() == "FLICKER":
        return heroes.Flicker(level, stutter)
    elif hero_name.upper() == "FORTRESS":
        return heroes.Fortress(level, stutter)
    elif hero_name.upper() == "GLAIVE":
        return heroes.Glaive(level, stutter)
    elif hero_name.upper() == "GRACE":
        return heroes.Grace(level, stutter)
    elif hero_name.upper() == "MIHO":
        return heroes.Miho(level, stutter)
    else:
        raise Exception(f"Invalid hero name '{hero_name}' - misspelling, malformed or not implemented")


def create_player(hero_name, build, level, stutter):
    if not 1 <= level <= 12:
        raise Exception(f"Invalid level '{level}' - valid values are in range [1, 12]")
    item_objs = list()
    for item in build:
        item_objs.append(create_item(item))
    hero_obj = create_hero(hero_name, level, stutter)
    hero_obj.init_build(item_objs)
    return hero_obj


def main(args):
    parser = argparse.ArgumentParser(
        prog="python3 simulate_combat.py",
        description="Generates a graph representing a 1v1 battle between two heroes",
        prefix_chars="-",
    )
    parser.add_argument(
        "hero_one",
        type=str,
        help="The first hero to engage in combat"
    )
    parser.add_argument(
        "hero_two",
        type=str,
        help="The second hero to engage in combat"
    )
    parser.add_argument(
        "--items_one",
        type=str,
        nargs="+",
        default="",
        help="The items Hero One has equipped"
    )
    parser.add_argument(
        "--items_two",
        type=str,
        nargs="+",
        default="",
        help="The items Hero Two has equipped"
    )
    parser.add_argument(
        "--level_one",
        type=int,
        default=1,
        help="The level of Hero One"
    )
    parser.add_argument(
        "--level_two",
        type=int,
        default=1,
        help="The level of Hero Two"
    )
    parser.add_argument(
        "--stutter_one",
        action='store_true',
        help="Hero One uses stutter stepping"
    )
    parser.add_argument(
        "--stutter_two",
        action='store_true',
        help="Hero Two uses stutter stepping"
    )
    args = parser.parse_args(args)
    hero_one = create_player(args.hero_one, args.items_one, args.level_one, args.stutter_one)
    hero_two = create_player(args.hero_two, args.items_two, args.level_two, args.stutter_two)
    h1_hp = list()
    h2_hp = list()
    h1_dmg = list()
    h2_dmg = list()
    milliseconds = 1
    while True:
        if hero_one.stats['current_hp'] <= 0 or hero_two.stats['current_hp'] <= 0:
            break
        h1_hp.append(hero_one.stats['current_hp'])
        h2_hp.append(hero_two.stats['current_hp'])
        h1_attack = hero_one.basic_attack(milliseconds)
        h2_attack = hero_two.basic_attack(milliseconds)
        h1_ack = hero_one.receive_attack(milliseconds, h2_attack)
        h2_ack = hero_two.receive_attack(milliseconds, h1_attack)
        hero_one.process_attack_ack(h2_ack)
        hero_two.process_attack_ack(h1_ack)
        h1_dmg.append(h2_ack["true_dmg"] + h2_ack["cp_dmg"] + h2_ack["wp_dmg"])
        h2_dmg.append(h1_ack["true_dmg"] + h1_ack["cp_dmg"] + h1_ack["wp_dmg"])
        milliseconds += 1
    plt.plot(h1_dmg, label=f"Hero 1: ({hero_one.name}) dmg to ({hero_two.name})")
    plt.plot(h1_hp, label=f"Hero 1: {hero_one.name} health points")
    plt.plot(h2_dmg, label=f"Hero 2: ({hero_two.name}) dmg to ({hero_one.name})")
    plt.plot(h2_hp, label=f"Hero 2: {hero_two.name} health points")
    plt.legend()
    plt.xlabel("Milliseconds")
    plt.ylabel("Points")
    plt.savefig(f"{hero_one.name}_vs_{hero_two.name}")


if __name__ == '__main__':
    main(argv[1:])
