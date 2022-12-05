# VainGlory Combat Simulation
This tool creates a visual representation of a 1v1 combat simulation.
Stats are taken from in game,
[this VGFire guide](https://www.vaingloryfire.com/vainglory/guide/a-beginners-guide-to-math-and-calculations-in-vainglory-with-updated-stats-for-objectives-creatures-and-minions-19763#AttackSpeed)
, and [VGFire Hero Wiki](https://www.vaingloryfire.com/vainglory/wiki/heroes).

Some information is not available online, so a best guess is in place. This is documented.

## Getting Started
Clone this repo or download the .zip archive. 

Some libraries are required for this tool. You can install them using this command:

    pip install -r requirements.txt

## How to Use This Tool
### Quick overview:    

    python3 simulate_combat.py [-h] [--items_one ITEMS_ONE [ITEMS_ONE ...]] [--items_two ITEMS_TWO [ITEMS_TWO ...]] [--level_one LEVEL_ONE] [--level_two LEVEL_TWO] [--stutter_one] [--stutter_two] hero_one hero_two

### Required Arguments
#### hero_one
Set the Hero for Hero One. [Read about the implemented heroes here](#implemented-heroes)

#### hero_two
Set the Hero for Hero One. [Read about the implemented heroes here](#implemented-heroes)

### Optional Arguments
#### --level_one
Set the level [1-12] for Hero One. 

#### --level_two
Set the level [1-12] for Hero Two.

#### --items_one
Hero One can have up to six items. The space-separated list after this flag will be used in the combat simulation. [Read
about the implemented items here.](#implemented-items)

#### --items_two
Hero Two can have up to six items. The space-separated list after this flag will be used in the combat simulation. [Read
about the implemented items here.](#implemented-items)

#### --stutter_one
Set if Hero One preforms perfect stutter steps.

#### --stutter_one
Set if Hero Two preforms perfect stutter steps.


## Implemented Heroes
As an argument for hero_one or hero_two, you can set the hero by typing one of these names (case insensitive)

If it is not on this list, it is not implemented yet.
- Amael
  - Abilities and hero perk not implemented
  - Attack Speed Factors estimated due to lack of documentation
- Adagio
  - Abilities and hero perk not implemented
- Alpha
  - Abilities and hero perk not implemented
- Anka
  - Abilities and hero perk not implemented
  - Attack Speed Factors estimated due to lack of documentation
- Ardan
  - Abilities and hero perk not implemented
- Baptiste
  - Abilities and hero perk not implemented
  - Attack Speed Factors estimated due to lack of documentation
- Baron
  - Abilities and hero perk not implemented
- Blackfeather
  - Abilities and hero perk not implemented
- Caine
  - Abilities and hero perk not implemented
  - Attack Speed Factors estimated due to lack of documentation
- Catherine
  - Abilities and hero perk not implemented
- Celeste
  - Abilities and hero perk not implemented
- Churnwalker
  - Abilities and hero perk not implemented
  - Attack Speed Factors estimated due to lack of documentation
- Flicker
  - Abilities and hero perk not implemented
- Fortress
  - Abilities and hero perk not implemented
- Glaive
  - Abilities and hero perk not implemented
- Grace
  - Abilities and hero perk not implemented
- Miho
  - Abilities and hero perk not implemented
  - Attack Speed Factors estimated due to lack of documentation

## Implemented Items
As an argument for after items_one or items_two, you can set the item by typing one of these names (case insensitive)

If it is not on this list, it is not implemented yet.
### Red Tree
- SorrowBlade
- PoisonedShiv
- SerpentsMask
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
- BoneSaw
- TornadoTrigger
- TyrantsMonocle

### Blue Tree
- not implemented

### Defense
- not implemented
- 
### Utility
- not implemented
- 
### Consumables
- not implemented