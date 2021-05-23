import sys, time, argparse
from random import randint

import interfaceUtils as iu
import lookup

from foodtable import FoodTable
import krakenUtils as utils


minimum_side = 32

parser = argparse.ArgumentParser(description="Build a Minecraft Settlement, by Claus Aranha (2021)")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--player", help="build the settlement around the player's current location",
                   action="store_true")
group.add_argument("-b", "--buildarea", help="build the settlement on the area defined by the 'setbuildarea' http mod command",
                   action="store_true")
group.add_argument("-c", "--coordinates", nargs = 6, type=int,
                   metavar=('x0', 'y0', 'z0', 'x1', 'y1', 'z1'),
                   help="build the settlement on the area defined by these coordinates")
parser.add_argument("-r", "--radius", type=int, default="64", metavar="R",
                    help="Radius for building area, only meaningful with -p")
args = parser.parse_args()

def getBuildArea(args):
    if (args.player):
        _r = args.radius*2
        area = iu.requestPlayerArea(_r, _r)
    elif (args.buildarea):
        area = iu.requestBuildArea()
    elif (args.coordinates):
        x0, y0, z0, x1, y1, z1 = args.coordinates
        iu.setBuildArea(*(args.coordinates))
        area = iu.requestBuildArea()

    smallest_side = min(abs(area[0] - area[3]), abs(area[2] - area[5]))
    if smallest_side < minimum_side:
        raise ValueError("Smallest side of user-defined build area is too small (should be at least {})".format(minimum_side))
    return area


if __name__ == "__main__":
    print("The Kraken has been released!")

    starttime = time.time()
    buildarea = getBuildArea(args)
    center = ((buildarea[0]+buildarea[3])//2,
              (buildarea[2]+buildarea[5])//2)
    print("BuildArea is {}, centered around {}.".format(buildarea,center))

    # Creating world datafiles
    iu.makeGlobalSlice()
    ws = iu.globalWorldSlice
    ft = FoodTable(ws)

    # Select Kraken Location

    location = [];
    for _ in range(10):
        _x, _z = randint(buildarea[0], buildarea[3]), randint(buildarea[2], buildarea[5])
        _y = ws.heightmaps["MOTION_BLOCKING_NO_LEAVES"][_x - buildarea[0],_z - buildarea[2]]+1
        while ws.getBlockAt(_x, _y, _z) in lookup.TRANSPARENT:
            _y -= 1

        _block = ws.getBlockAt(_x, _y, _z)
        _food = ft.getFood(_x, _y, _z)

        _score = _food + _y/20 + utils.mdist2d(_x, _z, *center)
        location.append((-1*_score, (_x, _y, _z)))
    location.sort()

    location = location[0][1]

    print("The Kraken has landed at {}.".format(location))



    endtime = time.time()
    print("Total time was {:.2} seconds".format(endtime - starttime))
