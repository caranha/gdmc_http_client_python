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
- [X] Depth First Search
  - Starting from the "trunk", put nodes on priority queue (distance + food)
    - priority queue nodes are discarded if fully in air, or fully in stone
    - distance should have higher priority than food
    - there should be a little bit of randomness
  - After finishing the DFS, add food to food bank, and path to "roots"
    - union of roots makes "body"

## Action-Based Growth
  - Consume: Transform energy into body mass, body mass is used for evolution
             Amount of consumption depends on existing structures (legs, nodes)
  - New Leg: Costs a lot of Energy, creates a new leg from a node using DFS
  - Absorb: Costs little Energy, draws food from random block around the leg.
            Leg grows thicker.
  - Expand: Costs some energy, creates a lv 1 node in one of this node's legs.
  - Upgrade: Costs some energy, upgrades a node,
       A node lv n can support up to k_n nodes of level n-1
       A node lv n costs n^2 x something energy

  - Logic:
    - If any node has no legs, create 5 legs from that node
    - If energy is low, Absorb from a high energy leg, update leg energy
    - If there is enough energy, and spare capacity, create a new node
      on high energy leg.
    - If there is enough energy, and no new nodes are possible,
      try the most expensive upgrade possible

  - Leg Growth:
    Select random neighbor blocks of the leg, add their food to
    the creature. Replace random blocks of the leg into their "next stage"
    (create "next stage" function)
    - If leg has no more food, start to transform it into soul sand and bone
  - Node Growth: Expand the trunk to all sizes, and add more spires at random
    location. Add lights and nether vines in random locations as necessary.



## Simple Player House

## Central Node and Evolution

## Better Player House

## Better fungus

# TODO Notes
- Reduce probability of taking a step underground?
  (Try to keep at least one face near air?)
- Extend food table with missing blocks
- Should I add the pheromon of all ants, or only the maximum?
