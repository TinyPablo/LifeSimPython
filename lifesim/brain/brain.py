from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from lifesim.brain.connection import ConnectionEndType, ConnectionTipType
from lifesim.brain.genome import Genome
from lifesim.brain.neuron import Neuron
from lifesim.brain.neuron_type import NeuronType
from lifesim.brain.neurons import get_fresh_neurons

if TYPE_CHECKING:
    from lifesim.common.typing import Entity

class Brain:
    def __init__(self, genome: Genome, entity: Entity) -> None:
        self.genome: Genome = genome
        self.entity: Entity = entity
        
        self.neurons: list[Neuron] = []
        self.brain_str: str = ''

    def __str__(self) -> str:
        return self.brain_str
    
    def __repr__(self):
        return self.__str__()

    @property
    def input_neurons(self) -> list[Neuron]:
        return [n for n in self.neurons if n.type == NeuronType.INPUT]
    
    @property
    def output_neurons(self) -> list[Neuron]:
        return [n for n in self.neurons if n.type == NeuronType.OUTPUT]
    
    @property
    def internal_neurons(self) -> list[Neuron]:
        return [n for n in self.neurons if n.type == NeuronType.INTERNAL]
    
    def connect_neurons(self) -> None:
        self.brain_str = ''
        genes = self.genome.genes
        assert genes is not None  # for mypy
        # print(genes)

        for gene in genes:
            input_neuron_list: list[Neuron] = list()
            output_neuron_list: list[Neuron] = list()

            if gene.conn_tip_neuron_type == ConnectionTipType.INPUT or not self.internal_neurons:
                input_neuron_list = self.input_neurons
            elif gene.conn_tip_neuron_type == ConnectionTipType.INTERNAL:
                input_neuron_list = self.internal_neurons

            if gene.conn_end_neuron_type == ConnectionEndType.OUTPUT or not self.internal_neurons:
                output_neuron_list = self.output_neurons
            elif gene.conn_end_neuron_type == ConnectionEndType.INTERNAL:
                output_neuron_list = self.internal_neurons
            
            input_neuron: Neuron = input_neuron_list[gene.conn_tip_neuron_id % len(input_neuron_list)]
            output_neuron: Neuron = output_neuron_list[gene.conn_end_neuron_id % len(output_neuron_list)]
            
            try:
                # print("Trying to connect neurons:")
                # print(f'INPUT NEURON: ({input_neuron.type.name}) "{input_neuron.name}"')
                # print('AND')
                # print(f'OUTPUT NEURON: ({output_neuron.type.name}) "{output_neuron.name}"')
                # print(f'Potential connection weight: <{gene.conn_weight}>')
                
                Neuron.connect_neurons(input_neuron, output_neuron, gene.conn_weight) 
                # print(f"STATUS: <SUCCESS>")
            except ValueError:
                pass
                # print("STATUS <FAILED>")
                # print(f'Reason: {e}')
            self.brain_str += f'{input_neuron.name} {output_neuron.name} {gene.conn_weight:.2f}\n'



    def init(self) -> None:
        self.neurons = get_fresh_neurons(self.entity.simulation.settings)
        self.connect_neurons()
        Neuron.sort(self.neurons)
        Neuron.filter_and_prune(self.neurons)

    def process(self) -> None:
        def _noop(): 
            return None
        
        final_action: Callable = _noop
        final_action_chance: float = float('-inf')
        
        for n in self.neurons:

            if n.type == NeuronType.INPUT:
                n.execute_as_input_neuron(self.entity)

            elif n.type == NeuronType.INTERNAL:
                n.execute_as_internal_neuron()

            elif n.type == NeuronType.OUTPUT:
                n.execute_as_output_neuron(self.entity)

        try:
            final_action(self.entity)
        except Exception:
            pass