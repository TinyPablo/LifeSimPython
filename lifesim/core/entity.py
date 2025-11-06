from __future__ import annotations

from typing import TYPE_CHECKING

from lifesim.brain.genome import Genome
from lifesim.core.transform import Transform

if TYPE_CHECKING:
    from lifesim.core.grid import Grid
    from lifesim.core.simulation import Simulation


class Entity:
    def __init__(self, genome: Genome, simulation: Simulation) -> None:
        from lifesim.brain.brain import Brain 
        
        self.brain: Brain = Brain(genome, self)
        self.transform: Transform = Transform()
        self.dead: bool = False
        self.simulation: Simulation = simulation
        self.grid: Grid | None = None
        self.performed_actions: set[str] = set()

    def __str__(self) -> str:
        return f"E(dead={self.dead})"
    
    __repr__ = __str__
    

    @staticmethod
    def int_to_color(n: int) -> tuple[int, int, int]:
        r_bits = (n >> 22) & 0x3FF
        g_bits = (n >> 12) & 0x3FF
        b_bits = (n >> 2) & 0x3FF

        r = int(r_bits / 0x3FF * 255)
        g = int(g_bits / 0x3FF * 255)
        b = int(b_bits / 0x3FF * 255)

        return r, g, b

    @property
    def color(self) -> tuple[int, int, int]:
        genes = self.brain.genome.genes
        assert genes is not None  # for mypy
        avg_gene: int = int(sum([int(g) for g in genes]) / len(genes))
        return Entity.int_to_color(avg_gene)

    def die(self) -> None:
        self.simulation.grid.remove_entity(self.transform.position_x, self.transform.position_y)
        self.dead = True

    def set_position(self, x: int, y: int) -> None:
        self.transform.position_x = x
        self.transform.position_y = y