import numpy as np
import random
from queue import PriorityQueue

from krakenUtils import mdist2d, idx2coord


import lookup
from toolbox import loop3d


class DFS:
    def __init__(self, worldslice, foodtable, center):
        self.rect = worldslice.rect
        self.ws = worldslice
        self.ft = foodtable
        self.center = center
        self.depth = 30
        self.score = 0
        self.trunk = set()
        self.trunk.add(center)

    def g2l(self, x, y, z):
        return (x - self.rect[0], y, z-self.rect[1])

    def inBounds(self, x, y, z):
        return (x >= self.rect[0] and x < self.rect[0]+self.rect[2] and
                z >= self.rect[1] and z < self.rect[1]+self.rect[3])

    def visit(self, pos, toVisit, pq):
        food = self.ft.getFood(*pos);
        self.ft.changeFood(*pos, -1*food)
        newNodes = []

        allair, noair = True, True  # Do no add nodes from here if we're enceased in air or stone

        for _i in loop3d(*(pos - np.ones(3, dtype = int)), *(pos + np.ones(3, dtype = int))):
            if (not _i in toVisit and self.inBounds(*_i)):
                _dist = mdist2d(_i[0], _i[2], self.center[0], self.center[2])
                _food = self.ft.getFood(*_i)
                prio = _dist + _food / 5 + random.random() * 5
                newNodes.append((-1*prio, _i))
                block = self.ws.getBlockAt(*_i)
                if "air" in block:
                    noair = False
                else:
                    allair = False
                if "netherrack" in block: # netherrack counts as air for us
                    noair = False

        if not (allair or noair):
            for _i in newNodes:
                toVisit.add(_i[1])
                pq.put_nowait(_i)

        return food

    def runDFS(self, start, steps = None):
        if steps is None:
            steps = self.depth
        food = 0
        pq = PriorityQueue()
        visitSet = set()
        visited = set()
        visitSet.add(start)
        pq.put((0, start))
        while (steps > 0 and pq.qsize() > 0):
            next = pq.get_nowait()
            visited.add(next[1])

            food += self.visit(next[1], visitSet, pq)
            steps -= 1

        return(food, visited)


    def runIteration(self):
        pass
