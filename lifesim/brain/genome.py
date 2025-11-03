from __future__ import annotations

from lifesim.brain.gene import Gene
from lifesim.utils.rng import rng

class Genome:
    def __init__(self, size: int | None = None, genes: list[Gene] | None = None) -> None:
        self.genes: list[Gene] | None = None
        self.size: int | None = size

        if genes is None:
            self.randomize()
        else:
            self.genes = genes

    def randomize(self) -> None:
        if self.size is None:
            raise ValueError("Genome size cannot be None when randomizing")
        self.genes = [Gene() for _ in range(self.size)]

    def __str__(self) -> str:
        assert self.genes is not None  # for mypy
        return '\n'.join(str(g) for g in self.genes)
    
    def __iter__(self):
        assert self.genes is not None  # for mypy
        return iter(self.genes)

    @staticmethod
    def crossover(genome_a: Genome, genome_b: Genome, mutation_probability: float) -> Genome:
        assert genome_a.genes is not None and genome_b.genes is not None  # for mypy

        len_a = len(genome_a.genes)
        len_b = len(genome_b.genes)

        half_len_a = max(1, len_a // 2)
        half_len_b = max(1, len_b // 2)

        half_a = rng.random.sample(genome_a.genes, half_len_a)
        half_b = rng.random.sample(genome_b.genes, half_len_b)
        
        genes: list[Gene] = [Gene(data.gene) for data in half_a] + [Gene(data.gene) for data in half_b]
        
        for gene in genes:
            gene.try_mutate(mutation_probability)
            
        return Genome(genes=genes)