from __future__ import annotations

from enum import Enum

from lifesim.utils.rng import rng


class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (1, -1)
    DOWN_LEFT = (-1, 1)
    DOWN_RIGHT = (1, 1)

    @staticmethod
    def random() -> Direction:
        return rng.random.choice(list(Direction))