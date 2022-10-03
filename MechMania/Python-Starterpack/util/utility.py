from enum import Enum
import math
import random
import numpy as np

import config

from game.position import Position

def manhattan_distance(p1: Position, p2: Position) -> int:
    return np.abs(p1.x - p2.x) + np.abs(p1.y - p2.y)

def chebyshev_distance(p1: Position, p2: Position) -> int:
    #return p1.x
    if(np.abs(p1.x - p2.x) > np.abs(p1.y - p2.y)):
        return np.abs(p1.x - p2.x)
    else:
        return np.abs(p1.y - p2.y)
    #return np.max(np.abs(p1.x - p2.x), np.abs(p1.y - p2.y))

def in_bounds(p: Position) -> bool:
    #  Assume board runs from 0 to BOARD_SIZE - 1
    return ((p.x >= 0) and (p.x < config.BOARD_SIZE) and (p.y >= 0) and (p.y < config.BOARD_SIZE))

def random_enum(clazz: Enum):
    return random.choice(list(clazz))