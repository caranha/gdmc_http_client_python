import numpy as np
import lookup
from toolbox import loop3d
from krakenUtils import mdist2d, idx2coord

## PARAMETERS
FOODGATHERED = 20
MAXSTEPS = 50
PHEROMONEDECAY = 0.8

## BLOCK HARDNESS
IMPASSABLE = ("minecraft:stone", "minecraft:granite", "minecraft:diorite", "minecraft:andesite")
AIR = ("minecraft:water",) + lookup.INVISIBLE

HARDNESS = {
    0: IMPASSABLE,
    .2: AIR,
}

def hardnessLookup(blockname):
    for value, blocks in HARDNESS.items():
        if blockname in blocks:
            return value
    return 1
## BLOCK HARDNESS

class ACO:
    def __init__(self, worldslice, foodtable, center, ants = 60):
        self.rect = worldslice.rect
        self.ws = worldslice
        self.ft = foodtable
        self.center = center
        self.phero = np.zeros((self.rect[2]+1, 255, self.rect[3]+1))
        self.ants = ants

    def probMatrix(self, pos, path):
        phe = np.zeros((3, 3, 3))
        prob = np.ones((3, 3, 3))
        hardness = np.zeros((3, 3, 3))
        past = np.ones((3, 3, 3))
        dist = np.zeros((3, 3, 3))

        for _i in loop3d(3,3,3):
            _pos = pos + (_i - np.ones(3, dtype=int))
            try:
                phe[_i] = self.phero[_pos[0] - self.rect[0], _pos[1], _pos[2] - self.rect[1]]
                hardness[_i] = hardnessLookup(self.ws.getBlockAt(*_pos))
            except IndexError: # zero chance of going out of bounds
                phe[_i] = 0
                hardness[_i] = 0
            if (tuple(_pos) in path):
                past[_i] = 0
            dist[_i] = mdist2d(_pos[0], _pos[2], self.center[0], self.center[2])

        prob = (prob + phe + dist)*hardness*past
        # print("phe", phe)
        # print("hard", hardness)
        # print("past", past)
        # print("dist", dist)
        return(prob)

    def runAnt(self):
        steps = 0
        pos = np.array(self.center, dtype = int)
        path = [self.center]
        while(steps < MAXSTEPS):
            if (self.ft.getFood(*pos) > 0): # end walk if we found food
                break

            allair, noair = True, True # end walk if we are underground or in air
            for _i in loop3d(3,3,3):
                block = self.ws.getBlockAt(*(pos + _i - np.ones(3, dtype = int)))
                if "air" in block:
                    noair = False
                else:
                    allair = False
                if "netherrack" in block: # netherrack counts as air for us
                    noair = False
            if (allair or noair):
                break

            prob = self.probMatrix(pos,path)
            if (prob.sum == 0):
                break

            idx = np.random.choice(27, p = prob.flatten() / prob.sum())
            pos = pos + idx2coord(idx) - np.ones(3, dtype=int)
            steps += 1
            path.append(tuple(pos))

        return path

    def runIteration(self):
        newphero = np.zeros((self.rect[2]+1, 255, self.rect[3]+1))
        totalfood = 0
        steps = set()
        for a in range(self.ants):
            path = self.runAnt()
            #print("Ant {}: {}".format(a,path))
            gfood = self.ft.getFood(*(path[-1]))
            if gfood > 0:
                totalfood += gfood
                self.ft.changeFood(*(path[-1]), -1*gfood)

            pheroadd = gfood + mdist2d(path[-1][0], path[-1][2], self.center[0], self.center[2])
            #print("Pheromone: {}".format(pheroadd))
            for p in path:
                steps.add(p)
                _lp = (p[0] - self.rect[0], p[1], p[2] - self.rect[1])
                newphero[_lp] += pheroadd
        self.phero = self.phero*PHEROMONEDECAY + newphero
        return steps
