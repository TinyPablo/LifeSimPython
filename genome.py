import random
import time
from typing import List, Optional
from gene import Gene
from simulation_settings import settings


class Genome:
    def __init__(self, size: Optional[int] = None, genes: Optional[list[Gene]] = None) -> None:
        self.genes: List[Gene] = None
        self.size: Optional[int] = size
        if genes is None:
            self.randomize()
        else:
            self.genes = genes

    def randomize(self) -> None:
        if self.size is None:
            raise Exception('None exception')
        self.genes = [Gene() for _ in range(self.size)]

    def __str__(self) -> str:
        return '\n'.join([str(g) for g in self.genes])
    
    def __iter__(self):
        return iter(self.genes)

    @staticmethod
    def crossover(genome_a: 'Genome', genome_b: 'Genome') -> 'Genome':
        len_a = len(genome_a.genes)
        len_b = len(genome_b.genes)

        half_len_a = max(1, len_a // 2)
        half_len_b = max(1, len_b // 2)

        half_a = random.sample(genome_a.genes, half_len_a)
        half_b = random.sample(genome_b.genes, half_len_b)
        
        genes: list[Gene] = [Gene(data.gene) for data in half_a]  + [Gene(data.gene) for data in half_b]

        for gene in genes:
            gene.try_mutate(settings.gene_mutation_chance)
        
        return Genome(genes=genes)



    # def crossover(genome_a: 'Genome', genome_b: 'Genome') -> 'Genome':
    #     half_len_a = len(genome_a.genes) // 2
    #     half_len_b = len(genome_b.genes) // 2

    #     half_a = genome_a.genes[half_len_a:]
    #     half_b = genome_b.genes[half_len_b:]
        
    #     genes: list[Gene] = half_a + half_b

    #     for gene in genes:
    #         gene.try_mutate(settings.gene_mutation_chance)

    #     return Genome(genes=genes)
    
    # def crossover(genome_a: 'Genome', genome_b: 'Genome') -> 'Genome':
    #     half_len_a = len(genome_a.genes) // 2
    #     half_len_b = len(genome_b.genes) // 2

    #     use_first_half_a = bool(random.randint(0, 1))
    #     use_first_half_b = bool(random.randint(0, 1))

    #     half_a = genome_a.genes[:half_len_a] if use_first_half_a else genome_a.genes[half_len_a:]
    #     half_b = genome_b.genes[:half_len_b] if use_first_half_b else genome_b.genes[half_len_b:]

    #     genes: list[Gene] = half_a + half_b


    #     return Genome(genes=genes)