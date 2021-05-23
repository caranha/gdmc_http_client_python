# Milestones
## Basic ACO
- [X] Make food table, and calculate food Matrix on Level
  - High food: Logs, Flowers, Mycelium = 60
  - Medium food: Leaves, Grass = 30
  - Low food: Podzol, Mossy stones = 10

- [X] Select random central location with view from the sky

- [X] Perform ACO from random location
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

## Better search
- [ ] Depth First Search
  - Starting from the "trunk", put nodes on priority queue (distance + food)
    - priority queue nodes are discarded if fully in air, or fully in stone
    - distance should have higher priority than food
    - there should be a little bit of randomness
  - After finishing the DFS, add food to food bank, and path to "roots"
    - union of roots makes "body"
  - Next DFS begins from any node in the "trunk", weighted by distance
    - after each iteration, "trunk" grows based on food

## Simple Player House

## Central Node and Evolution

## Better Player House

## Better fungus

# TODO Notes
- Reduce probability of taking a step underground?
  (Try to keep at least one face near air?)
- Extend food table with missing blocks
- Should I add the pheromon of all ants, or only the maximum?
