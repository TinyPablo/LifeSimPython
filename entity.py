from typing import List, TYPE_CHECKING, Tuple

from gene import Gene
from transform import Transform
from genome import Genome


if TYPE_CHECKING:
    from grid import Grid
    from simulation import Simulation


class Entity:
    def __init__(self, genome: 'Genome', simulation: 'Simulation', grid: 'Grid') -> None:
        from brain import Brain
        self.brain: 'Brain' = Brain(genome, self)
        self.transform: Transform = Transform()
        self.dead: bool = False
        self.simulation: 'Simulation' = simulation
        self.grid: 'Grid' = grid

    def __str__(self) -> str:
        return f'E {self.dead}'

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def int_to_color(n: int) -> Tuple[int, int, int]:
        r_bits = (n >> 22) & 0x3FF
        g_bits = (n >> 12) & 0x3FF
        b_bits = (n >> 2) & 0x3FF

        r = int(r_bits / 0x3FF * 255)
        g = int(g_bits / 0x3FF * 255)
        b = int(b_bits / 0x3FF * 255)

        return r, g, b

    @property
    def color(self) -> tuple[int, int, int]:
        genes: List[Gene] = self.brain.genome.genes
        avg_gene: int = int(sum([int(g) for g in genes]) / len(genes))
        return Entity.int_to_color(avg_gene)

    def die(self) -> None:
        self.grid.remove_entity(self.transform.position_x, self.transform.position_y)
        self.dead = True

    def set_position(self, x: int, y: int) -> None:
        self.transform.position_x = x
        self.transform.position_y = y
