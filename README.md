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

## WARN and ERROR messages
When running this tool, there are warning and error messages that may pop up.
The warnings are there to describe how the current implementation might affect the results.
The error messages are if there are errors in the command.

Both message types provide a code and a description of what is happening as the program runs.

## Note About Critical Hits
Critical Hits are calculated in terms of expected value. This means that for 100 damage with a 50% critical chance
and 50% critical damage, each hit is calculated as 100 * (1 + (0.5 * 0.5)) = 125 damage. This is to give
consistent and expected results.

## Note About Item Actives
Item actives trigger on certain events within the simulation. This is documented under each item it effects.
It is done this way so as to consider the use of actives, however, this may not be optimal play. Too much logic otherwise.
Someone can clone and implement this in a different way if they wish.

## Implemented Heroes
As an argument for hero_one or hero_two, you can set the hero by typing one of these names (case-insensitive)

***There are currently no abilities or hero perks implemented yet - This will come - as it is, some heros may appear weaker than in reality***

- **Amael**
- **Adagio**
- **Alpha**
- **Anka**
- **Ardan**
- **Baptiste**
- **Baron**
- **Blackfeather**
- **Caine**
- **Catherine**
- **Celeste**
- **Churnwalker**
- **Flicker**
- **Fortress**
- **Glaive**
- **Grace**
- **Miho**
- ***No other heroes yet***
  - Entering the numbers is grueling and horrible! 
  - Sorry! 
  - I'll get to this soon!

## Implemented Items
As an argument for after items_one or items_two, you can set the item by typing one of these names (case insensitive)
### Red Tree
- **BarbedNeedle**
- **BookOfEulogies**
- **BoneSaw**
  - Stacks decay one per 100ms after delay of not hitting (may be different than in-game)
- **BlazingSalvo**
- **BreakingPoint**
- **HeavySteel**
- **LuckyStrike**
- **MinionsFoot**
- **PiercingSpear**
- **PoisonedShiv**
  - The mortal wounds is implemented so that every second attack applies effect, while in-game, there must be two hits on
    the same target. You can ignore this as this is a 1v1 situation.
- **SixSins**
- **SerpentsMask**
- **SorrowBlade**
- **Spellsword**
- **SwiftShooter**
- **TensionBow**
- **TornadoTrigger**
- **TyrantsMonocle**
- **WeaponBlade**

### Blue Tree
- not implemented

### Defense
- **Aegis**
  - Active triggers when available to block stun or silence. 
    - This behaves exactly like reflex block. 
    - May not be optimal.
- **AtlasPauldron**
  - Active is used whenever available
- **CapacitorPlate**
  - Since 1v1, passive only helps the holder.
- **CelestialShroud**
- **CoatofPlates**
- **Crucible**
  - Active triggers when available to block stun or silence. 
      - Since 1v1, this behaves exactly like reflex block. 
      - May not be optimal.
- **Dragonheart**
- **FountainOfRenewal**
  - Activates when holder is less that 25% health. 
    - This may not be optimal
- **KineticShield**
- **Lifespring**
- **LightArmor**
- **LightShield**
- **MetalJacket**
  - It's unclear when the passive effect is supposed to be considered/if affects true damage when calculating the damage to be taken.
  - This tool assumes that the damage reduction from the passive:
    - Includes true damage
    - Is considered right before taking the damage.
- **Oakheart**
- **Pulseweave**
  - Current state of program assumes that heroes are right next to each other, thus maximizing the damage of this item.
  - "Sprint" active is not well documented. Assumes +2 move speed.
- **ProtectorContract**
  - Passive ability only activates on ability use and only affects teammates. 
    - Since no teammates in 1v1, passive is not implemented.
- **ReflexBlock**
  - Active triggers when available and an attack would otherwise stun or silence the holder. 
  - In the graph, this shows up as an change in health for effect duration.
- **RooksDecree**
  - Passive ability only activates on ability use and only affects teammates. 
    - Since no teammates in 1v1, passive is not implemented.
- **SlumberingHusk**
  - Fortified health is treated as doubling current health for effect duration.
  - In the graph, this shows up as an change in health for effect duration.
- **Warmail**


### Utility
- not implemented
- 
### Consumables
- not implemented