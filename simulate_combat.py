import matplotlib.pyplot as plt
import heroes, items
from sys import argv
import argparse


def create_item(item):
    if item.upper() == "SORROWBLADE":
        return items.SorrowBlade()
    else:
        raise Exception(f"Invalid hero name '{item}' - misspelling, malformed or not implemented")


def create_player(hero_name, build, level):
    if not 1 <= level <= 12:
        raise Exception(f"Invalid level '{level}' - valid values are in range [1, 12]")
    item_objs = list()
    for item in build:
        item_objs.append(create_item(item))
    if hero_name.upper() == "MIHO":
        hero_obj = heroes.Miho(level)
    else:
        raise Exception(f"Invalid hero name '{hero_name}' - misspelling, malformed or not implemented")
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
    args = parser.parse_args(args)
    hero_one = create_player(args.hero_one, args.items_one, args.level_one)
    hero_two = create_player(args.hero_two, args.items_two, args.level_two)
    h1_hp = list()
    h2_hp = list()
    h1_dmg = list()
    h2_dmg = list()
    milliseconds = 0
    while True:
        if hero_one.stats['current_hp'] <= 0 or hero_two.stats['current_hp'] <= 0:
            break
        h1_hp.append(hero_one.stats['current_hp'])
        h2_hp.append(hero_two.stats['current_hp'])
        h1_attack = hero_one.send_attack(milliseconds)
        h2_attack = hero_two.send_attack(milliseconds)
        h1_ack = hero_one.receive_attack(milliseconds, h2_attack)
        h2_ack = hero_two.receive_attack(milliseconds, h1_attack)
        hero_one.process_attack_ack(milliseconds, h2_ack)
        hero_two.process_attack_ack(milliseconds, h1_ack)
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
