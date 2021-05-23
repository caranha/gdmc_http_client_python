import numpy as np
import lookup

# Foodtable builds and keeps a table of how much food is available
# to the world. It loads foodvalues lazily from the worldslice

# Intermediate block groups
LOGS = ('minecraft:oak_log', 'minecraft:birch_log', 'minecraft:spruce_log',
        'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log')


# Food Block groups
NOFOOD = ('minecraft:sand', 'minecraft:dirt', 'minecraft:stone') + lookup.GLASS + lookup.AIR
LOWFOOD = ('minecraft:podzol',)
MEDIUMFOOD = ('minecraft:grass_block',) + lookup.LEAVES + lookup.GRASSES + lookup.VINES
HIGHFOOD = ('minecraft:mycelium',) + LOGS + lookup.FLOWERS + lookup.CROPS

# Food values for block groups
FOODVALUES = {
  0: NOFOOD,
  10: LOWFOOD,
  30: MEDIUMFOOD,
  60: HIGHFOOD,
}

def foodLookup(blockname):
    for value, blocks in FOODVALUES.items():
        if blockname in blocks:
            return value
    print("WARNING: block '{}' has no foodvalue (default 0)".format(blockname))
    return 0


class FoodTable:
    def __init__(self, worldslice):
        self.rect = worldslice.rect
        self.ws = worldslice
        self.table = np.ones((self.rect[2]+1, 255, self.rect[3]+1))*-1

    def g2l(self, x, y, z):
        return (x - self.rect[0], y, z-self.rect[1])

    def getFood(self, gx, gy, gz):
        x, y, z = self.g2l(gx, gy, gz)
        if (self.table[x, y, z] == -1):
            self.table[x, y, z] = foodLookup(self.ws.getBlockAt(gx, gy, gz))
        return self.table[x, y, z]

    def changeFood(self, gx, gy, gz, df):
        x, y, z = self.g2l(gx, gy, gz)
        self.table[x, y, z] = max(self.getFood(gx, gy, gz) + df, 0)
        return self.table[x, y, z]
