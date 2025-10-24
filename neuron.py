from math import tanh
from typing import Callable, Dict, List, Optional, Set, Tuple, Union
from entity import Entity
from neuron_type import NeuronType

class Neuron:
    def __init__(self, name: str, type: NeuronType, *, input_func: Optional[Callable] = None, output_func: Optional[Callable] = None) -> None:
        self.name: str = name
        self.type: NeuronType = type
        
        if self.type == NeuronType.INPUT and input_func is None:
            raise TypeError('INPUT NEURON requires input function')
        self.input_func: Optional[Callable] = input_func
        
        if self.type == NeuronType.OUTPUT and output_func is None:
            raise TypeError('OUTPUT NEURON requires output function')
        self.output_func: Optional[Callable] = output_func

        self.input_neurons: List['Neuron'] = []
        self.output_neurons: List['Neuron'] = []

        self.weights: Dict['Neuron', float] = {}

        self.output: Optional[float] = None 
        self.disabled: bool = False

    # def refresh(self) -> None:
    #     self.disabled = False

    def disable(self) -> None:
        self.disabled = True

    def __str__(self) -> str:
        input_names: List[str] = ', '.join([neuron.name for neuron in self.input_neurons])
        output_names: List[str] = ', '.join([neuron.name for neuron in self.output_neurons])

        input_names = 'NONE' if input_names == '' else input_names
        output_names = 'NONE' if output_names == '' else output_names
        return f'NEURON {self.name}" | INPUTS: ({input_names}) OUTPUTS: ({output_names})\n'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def execute_as_input_neuron(self, entity: Entity) -> None:
        neuron_output = self.input_func(entity)
        self.output = neuron_output

    def execute_as_output_neuron(self) -> tuple[Callable, float]:
            input_neurons_sum = sum([n.output * n.weights[self] for n in self.input_neurons])
            neuron_output = tanh(input_neurons_sum)

            return self.output_func, neuron_output

    def execute_as_internal_neuron(self) -> None:
            input_neurons_sum = sum([n.output * n.weights[self] for n in self.input_neurons])
            neuron_output = tanh(input_neurons_sum)
            self.output = neuron_output
    
    @staticmethod
    def connect_neurons(tip_neuron: 'Neuron', end_neuron: 'Neuron', connection_weight: float) -> None:
        if tip_neuron.type == NeuronType.OUTPUT:
            raise ValueError("TIP neuron cannot be OUTPUT NEURON")
        
        if end_neuron.type == NeuronType.INPUT:
            raise ValueError("END neuron cannot be INPUT NEURON")
        
        if tip_neuron == end_neuron:
            raise ValueError("INPUT NEURON cannot be OUTPUT NEURON (self connection)")
        
        if end_neuron in tip_neuron.input_neurons or tip_neuron in end_neuron.output_neurons:
            raise ValueError("Reverse connection is not allowed")
        
        if end_neuron in tip_neuron.output_neurons or tip_neuron in end_neuron.input_neurons:
            raise ValueError("Connection duplicate not allowed")

        tip_neuron.output_neurons.append(end_neuron)
        end_neuron.input_neurons.append(tip_neuron)
        
        if Neuron.detect_cycle(tip_neuron): 
            tip_neuron.output_neurons.remove(end_neuron) 
            end_neuron.input_neurons.remove(tip_neuron)
            raise ValueError("Adding this connection creates a cycle")
        
        tip_neuron.weights[end_neuron] = connection_weight 

    @staticmethod
    def detect_cycle(start: 'Neuron') -> bool:
        def visit(neuron: 'Neuron', visited: Set['Neuron'], rec_stack: Set['Neuron']) -> bool:
            if neuron not in visited:
                visited.add(neuron)
                rec_stack.add(neuron)

                for neighbor in neuron.output_neurons:
                    if neighbor not in visited and visit(neighbor, visited, rec_stack):
                        return True
                    elif neighbor in rec_stack:
                        return True

                rec_stack.remove(neuron)
            return False

        visited: Set[Neuron] = set()
        rec_stack: Set[Neuron] = set()
        return visit(start, visited, rec_stack)

    @staticmethod
    def sort(neurons: List['Neuron']):
        input_counts = {neuron: len(neuron.input_neurons) for neuron in neurons}

        sorted_neurons: List['Neuron'] = []
        no_incoming: List['Neuron'] = [n for n in neurons if input_counts[n] == 0]

        while no_incoming:
            n: Neuron = no_incoming.pop()
            sorted_neurons.append(n)

            for m in n.output_neurons:
                input_counts[m] -= 1
                if input_counts[m] == 0:
                    no_incoming.append(m)

        if len(sorted_neurons) != len(neurons):
            raise ValueError("Graph has at least one cycle, sorting is not possible")

        sorted_map = {neuron.name: index for index, neuron in enumerate(sorted_neurons)}
        neurons.sort(key=lambda neuron: sorted_map.get(neuron.name, float('inf')))

        return neurons
    
    @staticmethod
    def filter(neurons: List['Neuron']) -> None:
        for neuron in neurons:

            if neuron.type == NeuronType.INPUT:
                if not neuron.output_neurons:
                    neuron.disable()
                    continue

            if neuron.type == NeuronType.OUTPUT:
                if not neuron.input_neurons:
                    neuron.disable()
                    continue

            if neuron.type == NeuronType.INTERNAL:
                if not neuron.output_neurons:
                    neuron.disable()
                    continue

            if not (neuron.input_neurons or neuron.output_neurons):
                neuron.disable()
                continue