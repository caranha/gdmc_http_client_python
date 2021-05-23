# Milestones
## Basic ACO
- [X] Make food table, and calculate food Matrix on Level
  - High food: Logs, Flowers, Mycelium = 60
  - Medium food: Leaves, Grass = 30
  - Low food: Podzol, Mossy stones = 10

- [X] Select random central location with view from the sky

- [ ] Perform ACO from random location
  - Parameters:
    - Ants per iteration, Max Steps, Pheromone Decay
    - Food per ant
  - Move Probability:
    - Distance from center
    - Pheromone
    - Past move penalty (past move = 0)
    - Block penalty (stone = 0, netherrack = 1.5, air = 0.2, artificial = 0.3, wood = 0.6)
    - If all blocks around are air, end the ACO
    - If all blocks are prob 0, end the ACO
    - If found food, end the ACO
  - Pheromone return: Food found + (distance from center / maxsteps)

## Simple Player House

## Central Node and Evolution

## Better Player House

## Better fungus

# TODO Notes
- Extend food table with missing blocks
