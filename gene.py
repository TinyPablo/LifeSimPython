import random

from typing import Optional
from connection import ConnectionTipType, ConnectionEndType


class Gene:
    def __init__(self, gene: Optional[int] = None) -> None:
        self._gene: Optional[int] = None
        if gene is None:
            self.randomize()
        else:
            self._gene = gene

    @property
    def gene(self) -> int:
        if self._gene is None:
            raise Exception('Gene is None')
        return self._gene & 0xFFFF_FFFF
    
    @gene.setter
    def gene(self, value: int) -> None:
        self._gene = value

    def randomize(self) -> None:
        self.gene: int = random.randint(0, 0xFFFF_FFFF)

    def __int__(self) -> int:
        return self.gene

    def __str__(self) -> str:
        conn_tip_type_int: int = (self.gene >> 31) & 1
        conn_tip_neuron_id: int = (self.gene >> 24) & 0b111_1111 
        conn_end_type_int: int = (self.gene >> 23) & 1
        conn_tip_neuron_id: int = (self.gene >> 16) & 0b111_1111 
        conn_weight_raw_int: int = self.gene & 0xFFFF

        return (
            f'GENE {self.gene} {bin(self.gene)[2:].rjust(16, "0")}\n'
            # f'{(} {self.conn_tip_neuron_type.name}\n'
            # f'{(self.gene >> 24) & 0b111_1111}\n'
            # f'{(self.gene >> 23) & 1} {self.conn_end_neuron_type.name}\n'
            # f'{(self.gene >> 16) & 0b111_1111}\n' #1 101 0110
            f'{self.gene & 0xFFFF} {self.conn_weight}\n')

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def conn_tip_neuron_type(self) -> ConnectionTipType:
        if (self.gene >> 31) & 1:
            return ConnectionTipType.INPUT
        return ConnectionTipType.INTERNAL
    
    @property
    def conn_tip_neuron_id(self) -> int:
        return (self.gene >> 24) & 0b111_1111
    
    @property
    def conn_end_neuron_type(self) -> ConnectionEndType:
        if (self.gene >> 23) & 1:
            return ConnectionEndType.OUTPUT
        return ConnectionEndType.INTERNAL
    
    @property
    def conn_end_neuron_id(self) -> int:
        return (self.gene >> 16) & 0b111_1111  
    
    @property
    def conn_weight(self) -> float:
        n: int = self.gene & 0xFFFF
        return n / 0xFFFF * 8 - 4
    
    def try_mutate(self, probability: float):
        if random.random() < probability:
            self.flip_random_bit()

    def flip_random_bit(self) -> None:
        bit_position = random.randint(0, 31)
        mask = 1 << bit_position
        self.gene ^= mask