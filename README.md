# VainGlory Combat Simulation
This tool creates a visual representation of a 1v1 combat simulation.

## Getting Started
Clone this repo or download the .zip archive. 

Some libraries are required for this tool. You can install them using this command:

    pip install -r requirements.txt

## How to Use This Tool
### Quick overview:    

    python3 simulate_combat.py [-h] [--items_one ITEMS_ONE [ITEMS_ONE ...]] [--items_two ITEMS_TWO [ITEMS_TWO ...]] [--level_one LEVEL_ONE] [--level_two LEVEL_TWO] hero_one hero_two

### Required Arguments
#### hero_one
Set the Hero for Hero One. [Read about the implemented heroes here](#implemented-heroes)

#### hero_two
Set the Hero for Hero One. [Read about the implemented heroes here](#implemented-heroes)

### Optional Arguments
#### --items_one
Hero One can have up to six items. The space-separated list after this flag will be used in the combat simulation. [Read
about the implemented items here.](#implemented-items)

#### --items_two
Hero Two can have up to six items. The space-separated list after this flag will be used in the combat simulation. [Read
about the implemented items here.](#implemented-items)

#### --level_one
Set the level [1-12] for Hero One. 

#### --level_two
Set the level [1-12] for Hero Two.

## Implemented Heroes
As an argument for hero_one or hero_two, you can set the hero by typing one of these names (case insensitive)

If it is not on this list, it is not implemented yet.
- Miho
  - Abilities and hero perk not implemented

## Implemented Items
As an argument for after items_one or items_two, you can set the item by typing one of these names (case insensitive)

If it is not on this list, it is not implemented yet.
- Red Tree
  - SorrowBlade
  - PoisonedShiv
  - SerpentsMask
    - passive not implemented
  - WeaponBlade
  - BreakingPoint
  - BarbedNeedle
  - TensionBow
  - MinionsFoot
  - BookOfEulogies
  - PiercingSpear
  - LuckyStrike
  - HeavySteel
  - BlazingSalvo
  - SwiftShooter
  - SixSins
  - Spellsword
    - passive not implemented
  - BoneSaw
  - TornadoTrigger
  - TyrantsMonocle
- Blue Tree
  - not implemented
- Defense
  - not implemented
- Utility
  - not implemented
- Consumables
  - not implemented